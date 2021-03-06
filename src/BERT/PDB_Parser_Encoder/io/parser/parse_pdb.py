import logging
import math
import numpy as np

from Bio.PDB.Selection import unfold_entities

from src.BERT.PDB_Parser_Encoder.model.encoding import blopmap_encode_three_letter

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("PDB Parser")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


def get_contact_info(structure, path, chain, angstrom, residue_id):
    """
    fetches all required information for a given residue
    :param structure:
    :param path:
    :param chain:
    :param angstrom:
    :param residue_id:
    :return:
    """
    name = structure[0][chain][residue_id].get_resname()
    neighbourcount = neighbour_counter(structure[0], chain, residue_id, angstrom)
    secondary_struct = find_secondary_struct_of_residue(residue_id, path)
    contact_info = [blopmap_encode_three_letter(name), [residue_id, chain], [neighbourcount], secondary_struct, []]

    return contact_info


def neighbour_counter(structure, chain, residue_id, angstrom):
    """
    calculates the count of neighbours for a residue within a passed angstrom constraint
    :param structure:
    :param chain:
    :param residue_id:
    :param angstrom: maximal distance of two residues to be considered neighbours
    :return:
    """
    neighbourcount = 0
    for cha in structure:
        for res in cha:
            if not (res.id[1] in [residue_id - 1, residue_id, residue_id + 1]):
                atoms_in_res = get_atoms_of_res_sidechain(res)
                if len(atoms_in_res) != 0:
                    if compute_residue_distance(atoms_in_res,
                                                get_atoms_of_res_sidechain(structure[chain][residue_id])) <= angstrom:
                        neighbourcount += 1

    return neighbourcount


def get_atoms_of_res_sidechain(residue):
    """
    finds all atoms of a given sidechain for a residue
    removes C, O, N
    :param residue:
    :return:
    """
    atoms_in_res = unfold_entities(residue, 'A')
    for atom in atoms_in_res:
        if atom.get_name() in ['C', 'O', 'N']:
            atoms_in_res.remove(atom)

    return atoms_in_res


def compute_residue_distance(atoms_residue_a, atoms_residue_b):
    """
    computes the distance of two given atoms
    :param atoms_residue_a:
    :param atoms_residue_b:
    :return:
    """
    a_center = np.mean([atom.get_coord() for atom in atoms_residue_a], axis=0)
    b_center = np.mean([atom.get_coord() for atom in atoms_residue_b], axis=0)
    distance = math.sqrt(math.pow((a_center[0] - b_center[0]), 2)
                         + math.pow((a_center[1] - b_center[1]), 2)
                         + math.pow((a_center[2] - b_center[2]), 2))

    return distance


def find_secondary_struct_of_residue(residue_id, pdb_path):
    """
    searches the PDB file for the secondary structure of a given residue ID
    :param residue_id:
    :param pdb_path:
    :return:
    """
    f = open(pdb_path, 'r')
    content_list = f.readlines()
    for line in content_list:
        if line.startswith('HELIX') or line.startswith('SHEET'):
            line_content_list = []
            line_split = line.split(' ')
            for split in line_split:
                if split != '':
                    line_content_list.append(split)
            if line.startswith('HELIX'):
                if residue_id in range(int(line_content_list[5]), int(line_content_list[8]) + 1):
                    return [0, 1, 0]
            else:
                if len(line_content_list) in [12, 20]:
                    x = 6
                    y = 9
                else:
                    x = 5
                    y = 8
                try:
                    if residue_id in range(int(line_content_list[x]), int(line_content_list[y]) + 1):
                        return [1, 0, 0]
                except:
                    pass

    return [0, 0, 1]
