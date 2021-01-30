# It takes a file in the standard format and then call the Guide to Pharmacology database 
# for every protien in the file and creates a new file with only the drug data

# import pygtop
import csv
import os 

# All of this is from the pyGtoP library (it more or less is the entire library)
# The timeout was failing so I had to take all the code from it to rewrite the timeout
# Line 1282 starts the actual functional code you would want to look at
import json
import requests

ROOT_URL = "http://www.guidetopharmacology.org/services/"

def get_json_from_gtop(query, attempts=20):
    """Issues a query to the GtoP web services, and returns the resulting JSON.
    If it does not get a valid response, it will try again, and if it still
    doesn't get JSON back, it will return None.
    :param str query: The query to append to the base URL.
    :param int attempts: The number of attempts to make before giving up \
    (default is 5).
    :return: JSON object or None"""

    if not isinstance(attempts, int):
        raise TypeError(
         "attempts must be an integer greater than zero, not %s", str(attempts)
        )
    if attempts < 1:
        raise ValueError(
         "attempts must be an integer greater than zero, not %s", str(attempts)
        )

    try_count = 0
    while try_count < attempts:
        response = requests.get("%s%s" % (ROOT_URL, query),timeout=200)
        print("Try number: ", try_count)
        print(response.status_code)
        try:
            if response.status_code == 200 and len(response.text) > 1:
                return json.loads(response.text)
                # break
            else:
                raise ValueError
        except ValueError:
            if response.status_code == 204:
                break
            try_count += 1
    return None

def get_target_by_id(target_id):
    """Returns a Target object of the target with the given ID.
    :param int target_id: The GtoP ID of the Target desired.
    :rtype: :py:class:`Target`
    :raises: :class:`.NoSuchTargetError`: if no such target exists in the database"""

    if not isinstance(target_id, int):
        raise TypeError("target_id must be int, not '%s'" % str(target_id))
    json_data = get_json_from_gtop("targets/%i" % target_id)
    if json_data:
        return Target(json_data)
    else:
        raise NoSuchTargetError("There is no target with ID %i" % target_id)

def get_target_by_id(target_id):
    """Returns a Target object of the target with the given ID.
    :param int target_id: The GtoP ID of the Target desired.
    :rtype: :py:class:`Target`
    :raises: :class:`.NoSuchTargetError`: if no such target exists in the database"""

    if not isinstance(target_id, int):
        raise TypeError("target_id must be int, not '%s'" % str(target_id))
    json_data = gtop.get_json_from_gtop("targets/%i" % target_id)
    if json_data:
        return Target(json_data)
    else:
        raise NoSuchTargetError("There is no target with ID %i" % target_id)


def get_all_targets():
    """Returns a list of all targets in the Guide to PHARMACOLOGY database. This
    can take a few seconds.
    :returns: list of :py:class:`Target` objects"""

    json_data = gtop.get_json_from_gtop("targets")
    return [Target(t) for t in json_data]


def get_targets_by(criteria):
    """Get all targets which specify the criteria dictionary.
    :param dict criteria: A dictionary of `field=value` pairs. See the\
     `GtoP target web services page <http://www.guidetopharmacology.org/\
     webServices.jsp#targets>`_ for key/value pairs which can be supplied.
    :returns: list of :py:class:`Target` objects."""

    if not isinstance(criteria, dict):
        raise TypeError("criteria must be dict, not '%s'" % str(criteria))

    search_string = "&".join(["%s=%s" % (key, criteria[key]) for key in criteria])
    json_data = get_json_from_gtop("targets?%s" % search_string)
    if json_data:
        return [Target(t) for t in json_data]
    else:
        return []

class NoSuchTargetError(Exception):
    """The exception raised if a specific target is requested which does not
    exist."""
    pass




def get_target_by_name(name):
    """Returns the target which matches the name given.
    :param str name: The name of the target to search for. Note that synonyms \
    will not be searched.
    :rtype: :py:class:`Target`
    :raises:  :class:`.NoSuchTargetError`: if no such target exists in the database."""

    if not isinstance(name, str):
        raise TypeError("name must be str, not '%s'" % str(name))
    targets = get_targets_by({"name": name})
    if targets:
        return targets[0]
    else:
        raise NoSuchTargetError("There is no target with name %s" % name)


def get_target_family_by_id(family_id):
    """Returns a TargetFamily object of the family with the given ID.
    :param int family_id: The GtoP ID of the TargetFamily desired.
    :rtype: :py:class:`TargetFamily`
    :raises: :class:`.NoSuchTargetFamilyError`: if no such family exists in the database"""

    if not isinstance(family_id, int):
        raise TypeError("family_id must be int, not '%s'" % str(family_id))
    json_data = gtop.get_json_from_gtop("targets/families/%i" % family_id)
    if json_data:
        return TargetFamily(json_data)
    else:
        raise NoSuchTargetFamilyError("There is no Target Family with ID %i" % family_id)


def get_all_target_families():
    """Returns a list of all target families in the Guide to PHARMACOLOGY database.
    :returns: list of :py:class:`TargetFamily` objects"""

    json_data = gtop.get_json_from_gtop("targets/families")
    return [TargetFamily(f) for f in json_data]



def get_ligand_by_id(ligand_id):
    """Returns a Ligand object of the ligand with the given ID.
    :param int ligand_id: The GtoP ID of the Ligand desired.
    :rtype: :py:class:`Ligand`
    :raises: :class:`.NoSuchLigandError` if no such ligand exists in the database"""

    if not isinstance(ligand_id, int):
        raise TypeError("ligand_id must be int, not '%s'" % str(ligand_id))
    json_data = get_json_from_gtop("ligands/%i" % ligand_id)
    if json_data:
        return Ligand(json_data)
    else:
        raise TypeError("There is no ligand with ID %i" % ligand_id)




class Ligand:
    """A Guide to PHARMACOLOGY ligand object.
    :param json_data: A dictionary obtained from the web services."""


    def __init__(self, json_data):
        self.json_data = json_data
        self._ligand_id = json_data["ligandId"]
        self._name = json_data["name"]
        self._abbreviation = json_data["abbreviation"] if json_data["abbreviation"] else None
        self._inn = json_data["inn"]
        self._ligand_type = json_data["type"]
        self._species = json_data["species"]
        self._radioactive = json_data["radioactive"]
        self._labelled = json_data["labelled"]
        self._approved = json_data["approved"]
        self._withdrawn = json_data["withdrawn"]
        self._approval_source = json_data["approvalSource"]
        self._subunit_ids = json_data["subunitIds"]
        self._complex_ids = json_data["complexIds"]
        self._prodrug_ids = json_data["prodrugIds"]
        self._active_drug_ids = json_data["activeDrugIds"]


    def __repr__(self):
        return "<Ligand %i (%s)>" % (self._ligand_id, self._name)


    def ligand_id(self):
        """Returns the ligand's GtoP ID.
        :rtype: int"""

        return self._ligand_id


    # @strip_html
    def name(self):
        """Returns the ligand's name.
        :param bool strip_html: If ``True``, the name will have HTML entities stripped.
        :rtype: str"""

        return self._name


    # @strip_html
    def abbreviation(self):
        """Returns the ligand's abbreviated name.
        :param bool strip_html: If ``True``, the abbreviation will have HTML entities stripped.
        :rtype: str"""

        return self._abbreviation


    # @strip_html
    def inn(self):
        """Returns the ligand's INN name.
        :param bool strip_html: If ``True``, the name will have HTML entities stripped.
        :rtype: str"""

        return self._inn


    def ligand_type(self):
        """Returns the ligand's type.
        :rtype: str"""

        return self._ligand_type


    def species(self):
        """Returns the ligand's species, where appropriate.
        :rtype: str"""

        return self._species


    def radioactive(self):
        """Returns True if the ligand is radioactive.
        :rtype: bool"""

        return self._radioactive


    def labelled(self):
        """Returns True if the ligand is labelled.
        :rtype: bool"""

        return self._labelled


    def approved(self):
        """Returns True if the ligand is approved.
        :rtype: bool"""

        return self._approved


    def withdrawn(self):
        """Returns True if the ligand has been withdrawn.
        :rtype: bool"""

        return self._withdrawn


    # @strip_html
    def approval_source(self):
        """Returns the regulatory body that approved the ligand, where appropriate.
        :param bool strip_html: If ``True``, the name will have HTML entities stripped.
        :rtype: str"""

        return self._approval_source


    def subunit_ids(self):
        """Returns the the ligand IDs of all ligands which are subunits of this
        target.
        :returns: list of ``int``"""

        return self._subunit_ids


    def subunits(self):
        """Returns a list of all ligands which are subunits of this ligand.
        :returns: list of :py:class:`Ligand` objects"""

        return [get_ligand_by_id(id_) for id_ in self._subunit_ids]


    def complex_ids(self):
        """Returns the the ligand IDs of all ligands of which this target is a
        subunit.
        :returns: list of ``int``"""

        return self._complex_ids


    def complexes(self):
        """Returns a list of all ligands of which this ligand is a subunit.
        :returns: list of :py:class:`Ligand` objects"""

        return [get_ligand_by_id(id_) for id_ in self._complex_ids]


    def prodrug_ids(self):
        """Returns the the ligand IDs of all ligands which are prodrugs of this
        ligand.
        :returns: list of ``int``"""

        return self._prodrug_ids


    def prodrugs(self):
        """Returns a list of all ligands which are prodrugs of this ligand.
        :returns: list of :py:class:`Ligand` objects"""

        return [get_ligand_by_id(id_) for id_ in self._prodrug_ids]


    def active_drug_ids(self):
        """Returns the the ligand IDs of all ligands which are active
        equivalents of this ligand.
        :returns: list of ``int``"""

        return self._active_drug_ids


    def active_drugs(self):
        """Returns a list of all ligands which are active equivalents of this ligand.
        :returns: list of :py:class:`Ligand` objects"""

        return [get_ligand_by_id(id_) for id_ in self._active_drug_ids]


    def iupac_name(self):
        """Returns the ligand's IUPAC name.
        :rtype: str"""

        return self._get_structure_json().get("iupacName")


    def smiles(self):
        """Returns the ligand's SMILES string.
        :rtype: str"""

        return self._get_structure_json().get("smiles")


    def inchi(self):
        """Returns the ligand's InChI string.
        :rtype: str"""

        return self._get_structure_json().get("inchi")


    def inchi_key(self):
        """Returns the ligand's InChI key.
        :rtype: str"""

        return self._get_structure_json().get("inchiKey")


    def one_letter_sequence(self):
        """Returns the ligand's single letter amino acid sequence where appropriate.
        :rtype: str"""

        return self._get_structure_json().get("oneLetterSeq")


    def three_letter_sequence(self):
        """Returns the ligand's three letter amino acid sequence where appropriate.
        :rtype: str"""

        return self._get_structure_json().get("threeLetterSeq")


    def post_translational_modifications(self):
        """Returns any post-translational modifications.
        :rtype: str"""

        return self._get_structure_json().get("postTranslationalModifications")


    def chemical_modifications(self):
        """Returns any chemical modifications.
        :rtype: str"""

        return self._get_structure_json().get("chemicalModifications")


    def hydrogen_bond_acceptors(self):
        """Returns the number of hydrogen bond accepting atoms.
        :rtype: int"""

        return self._get_molecular_json().get("hydrogenBondAcceptors")


    def hydrogen_bond_donors(self):
        """Returns the number of hydrogen bond donor atoms.
        :rtype: int"""

        return self._get_molecular_json().get("hydrogenBondDonors")


    def rotatable_bonds(self):
        """Returns the number of rotatable bonds in the ligand.
        :rtype: int"""

        return self._get_molecular_json().get("rotatableBonds")


    def topological_polar_surface_area(self):
        """Returns the polar surface area of the ligand in Angstroms.
        :rtype: float"""

        return self._get_molecular_json().get("topologicalPolarSurfaceArea")


    def molecular_weight(self):
        """Returns the ligand's mass in Daltons.
        :rtype: float"""

        return self._get_molecular_json().get("molecularWeight")


    def log_p(self):
        """Returns the logP value of the ligand.
        :rtype: int"""

        return self._get_molecular_json().get("logP")


    def lipinski_rules_broken(self):
        """Returns the number of Lipinski's Rules the ligand breaks.
        :rtype: int"""

        return self._get_molecular_json().get("lipinskisRuleOfFive")


    # @strip_html
    def synonyms(self):
        """Returns the number ligand's synonyms
        :returns: list of ``str``"""

        return [synonym["name"] for synonym in self._get_synonym_json()]


    def general_comments(self):
        """Returns general comments pertaining to the ligand.
        :rtype: str"""

        return self._get_comments_json().get("comments")


    def bioactivity_comments(self):
        """Returns comments pertaining to bioactivity.
        :rtype: str"""

        return self._get_molecular_json().get("bioactivityComments")


    def clinical_use_comments(self):
        """Returns comments pertaining to clinical use.
        :rtype: str"""

        return self._get_molecular_json().get("clinicalUse")


    def mechanism_of_action_comments(self):
        """Returns comments pertaining to mechanism.
        :rtype: str"""

        return self._get_molecular_json().get("mechanismOfAction")


    def absorption_and_distribution_comments(self):
        """Returns comments pertaining to absorption and distribution.
        :rtype: str"""

        return self._get_molecular_json().get("absorptionAndDistribution")


    def metabolism_comments(self):
        """Returns comments pertaining to metabolism.
        :rtype: str"""

        return self._get_molecular_json().get("metabolism")


    def elimination_comments(self):
        """Returns comments pertaining to elimination from the body.
        :rtype: str"""

        return self._get_molecular_json().get("elimination")


    def population_pharmacokinetics_comments(self):
        """Returns comments pertaining to population pharmacokinetics.
        :rtype: str"""

        return self._get_molecular_json().get("populationPharmacokinetics")


    def organ_function_impairments_comments(self):
        """Returns comments pertaining to organ function impairment.
        :rtype: str"""

        return self._get_molecular_json().get("organFunctionImpairment")


    def mutations_and_pathophysiology_comments(self):
        """Returns comments pertaining to mutations and pathophysiology.
        :rtype: str"""

        return self._get_molecular_json().get("mutationsAndPathophysiology")


    def database_links(self):
        """Returns a list of database links for this ligand.
        :rtype: list of :py:class:`.DatabaseLink`"""

        return [DatabaseLink(link_json) for link_json in self._get_database_json()]


    def interactions(self):
        """Returns a list of interactions for this ligand.
        :rtype: list of :py:class:`.Interaction`"""

        return [Interaction(interaction_json) for interaction_json in self._get_interactions_json()]


    # get_interaction_by_id = get_interaction_by_id
    """Returns an Interaction object of a given ID belonging to the ligand.
    :param int interaction_id: The interactions's ID.
    :rtype: :py:class:`.Interaction`
    :raises: :class:`.NoSuchInteractionError`: if no such interaction exists in the database."""


    def targets(self):
        """Returns a list of all targets which this ligand interacts with.
        :returns: list of :py:class:`.Target` objects"""

        targets = []
        for interaction in self.interactions():
            target = interaction.target()
            if target not in targets:
                targets.append(target)
        return targets


    # @pdb.ask_about_molecupy
    def gtop_pdbs(self):
        """Returns a list of PDBs which the Guide to PHARMACOLOGY says contain
        this ligand.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        pdbs = []
        for interaction in self.interactions():
            for pdb in interaction.gtop_pdbs():
                if pdb not in pdbs:
                    pdbs.append(pdb)
        return pdbs


    # @pdb.ask_about_molecupy
    def smiles_pdbs(self, search_type="exact"):
        """Queries the RSCB PDB database with the ligand's SMILES string.
        :param str search_type: The type of search to run - whether exact matches\
        only should be returned.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if self.smiles():
            xml = pdb.query_rcsb("smilesQuery", {
             "smiles": self.smiles(),
             "search_type": search_type
            })
            if xml:
                ligand_elements = list(xml[0])
                return [element.attrib["structureId"] for element in ligand_elements]
            else:
                return []
        else:
            return []


    # @pdb.ask_about_molecupy
    def inchi_pdbs(self):
        """Queries the RSCB PDB database with the ligand's InChI string.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if self.inchi():
            results = pdb.query_rcsb_advanced("ChemCompDescriptorQuery", {
             "descriptor": self.inchi(),
             "descriptorType": "InChI"
            })
            return results if results else []
        else:
            return []


    # @pdb.ask_about_molecupy
    def name_pdbs(self, comparator="equals"):
        """Queries the RSCB PDB database with the ligand's name.
        :param str comparator: The type of search to run - whether exact matches\
        only should be returned, or substrings etc.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        results = pdb.query_rcsb_advanced("ChemCompNameQuery", {
         "comparator": comparator.title(),
         "name": self.name(),
         "polymericType": "Any"
        })
        return results if results else []


    # @pdb.ask_about_molecupy
    def sequence_pdbs(self):
        """Queries the RSCB PDB database with the ligand's amino acid sequence,\
        if that ligand is a peptide.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if self.one_letter_sequence():
            results = pdb.query_rcsb_advanced("SequenceQuery", {
             "sequence": self.one_letter_sequence(),
             "eCutOff": "0.01",
             "searchTool": "blast",
             "sequenceIdentityCutoff": "100"
            })
            return results if results else []
        else:
            return []


    # @pdb.ask_about_molecupy
    def het_pdbs(self):
        """Queries the RSCB PDB database with the ligand's amino acid sequence,\
        if that ligand is a peptide.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        het = [h for h in self.database_links() if "PDB" in h.database()]
        if het:
            results = pdb.query_rcsb_advanced("ChemCompIdQuery", {
             "chemCompId": het[0].accession(),
            })
            return results if results else []
        else:
            return []


    # @pdb.ask_about_molecupy
    def all_external_pdbs(self):
        """Queries the RSCB PDB database by all parameters.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        return list(set(
         self.smiles_pdbs() +
         self.inchi_pdbs() +
         self.name_pdbs() +
         self.sequence_pdbs() +
         self.het_pdbs()
        ))


    # @pdb.ask_about_molecupy
    def all_pdbs(self):
        """Get a list of PDB codes using all means available - annotated and
        external.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        return list(set(
         self.gtop_pdbs() +
         self.all_external_pdbs()
        ))


    def find_in_pdb_by_smiles(self, molecupy_pdb):
        """Searches for the ligand in a `molecuPy <http://molecupy.readthedocs.io>`_
        PDB object by SMILES string and returns the small molecule it finds.
        :param molecupy_pdb: The molecuPy PDB object.
        :rtype: ``SmallMolecule``"""

        if self.smiles():
            formula = Counter([char.upper() for char in self.smiles()
             if char.isalpha() and char.upper() != "H"])
            matches = []
            for molecule in sorted(molecupy_pdb.model().small_molecules(), key=lambda m: m.molecule_id()):
                if molecule.formula() == formula:
                    matches.append(molecule)
            if matches:
                return sorted(matches,key=lambda m: len(m.bind_site().residues())
                 if m.bind_site() else 0, reverse = True)[0]


    def find_in_pdb_by_name(self, molecupy_pdb):
        """Searches for the ligand in a `molecuPy <http://molecupy.readthedocs.io>`_
        PDB object by ligand name and returns the small molecule it finds.
        :param molecupy_pdb: The molecuPy PDB object.
        :rtype: ``SmallMolecule``"""

        if self.name():
            matches = []
            for molecule in sorted(molecupy_pdb.model().small_molecules(), key=lambda m: m.molecule_id()):
                molecule_name = molecupy_pdb.data_file().het_names().get(molecule.molecule_name())
                if molecule_name and self.name().lower() == molecule_name.lower():
                    matches.append(molecule)
            if matches:
                return sorted(matches,key=lambda m: len(m.bind_site().residues())
                 if m.bind_site() else 0, reverse = True)[0]


    def find_in_pdb_by_mass(self, molecupy_pdb):
        """Searches for the ligand in a `molecuPy <http://molecupy.readthedocs.io>`_
        PDB object by ligand mass and returns the small molecule it finds.
        :param molecupy_pdb: The molecuPy PDB object.
        :rtype: ``SmallMolecule``"""

        if self.molecular_weight():
            molecules = sorted(
             list(molecupy_pdb.model().small_molecules()),
             key=lambda k: abs(k.mass() - self.molecular_weight())
            )
            if molecules and -40 < (molecules[0].mass() - self.molecular_weight()) < 40:
                return molecules[0]


    def find_in_pdb_by_peptide_string(self, molecupy_pdb):
        """Searches for the ligand in a `molecuPy <http://molecupy.readthedocs.io>`_
        PDB object by peptide sequence and returns the chain it finds.
        :param molecupy_pdb: The molecuPy PDB object.
        :rtype: ``Chain``"""

        if self.one_letter_sequence():
            for chain in molecupy_pdb.model().chains():
                if self.one_letter_sequence() in chain.sequence_string() and 0.9 <= (
                 len(self.one_letter_sequence()) / len(chain.sequence_string())
                ) <= 1:
                    return chain


    def _get_structure_json(self):
        json_object = get_json_from_gtop(
         "ligands/%i/structure" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_molecular_json(self):
        json_object = get_json_from_gtop(
         "ligands/%i/molecularProperties" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_synonym_json(self):
        json_object = get_json_from_gtop(
         "ligands/%i/synonyms" % self._ligand_id
        )
        return json_object if json_object else []


    def _get_comments_json(self):
        json_object = get_json_from_gtop(
         "ligands/%i/comments" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_database_json(self):
        json_object = get_json_from_gtop(
         "ligands/%i/databaseLinks" % self._ligand_id
        )
        return json_object if json_object else []


    def _get_interactions_json(self):
        json_object = get_json_from_gtop(
         "ligands/%i/interactions" % self._ligand_id
        )
        return json_object if json_object else []








class Interaction:
    """A Guide to PHARMACOLOGY interaction object.
    :param json_data: A dictionary obtained from the web services."""

    def __init__(self, json_data):
        self.json_data = json_data

        self._interaction_id = json_data["interactionId"]
        self._ligand_id = json_data["ligandId"]
        self._target_id = json_data["targetId"]
        self._species = json_data["targetSpecies"]
        self._primary_target = json_data["primaryTarget"]
        self._endogenous = json_data["endogenous"]
        self._interaction_type = json_data["type"]
        self._action = json_data["action"]
        affinity_values = "".join(
         [char for char in json_data["affinity"] if char in "0123456789. "]
        ).split()
        affinity_values = tuple(sorted([float(val) for val in affinity_values]))
        self._affinity_low = affinity_values[0] if affinity_values else None
        self._affinity_high = affinity_values[-1] if affinity_values else None
        self._affinity_type = json_data["affinityParameter"]


    def __repr__(self):
        return "<Interaction (%i --> %s %i)>" % (
         self._ligand_id,
         self._species,
         self._target_id
        )


    def interaction_id(self):
        """Returns the interaction's GtoP ID.
        :rtype: int"""

        return self._interaction_id


    def ligand_id(self):
        """Returns the GtoP ID of the associated ligand.
        :rtype: int"""

        return self._ligand_id


    def ligand(self):
        """Returns the Ligand object for this interaction.
        :rtype: :py:class:`.Ligand`"""

        # from .ligands import get_ligand_by_id
        try:
            return get_ligand_by_id(self._ligand_id)
        except TypeError:
            return None


    def target_id(self):
        """Returns the GtoP ID of the associated target.
        :rtype: int"""

        return self._target_id


    def target(self):
        """Returns the Target object for this interaction.
        :rtype: :py:class:`.Target`"""

        from .targets import get_target_by_id
        try:
            return get_target_by_id(self._target_id)
        except NoSuchTargetError:
            return None


    # @ask_about_molecupy
    def gtop_pdbs(self):
        """Returns a list of PDBs which the Guide to PHARMACOLOGY says contain
        this interaction.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        json_data = gtop.get_json_from_gtop("targets/%i/pdbStructure" % self._target_id)
        if json_data:
            return [
             pdb["pdbCode"] for pdb in json_data
              if pdb["species"].lower() == self._species.lower()
               and pdb["ligandId"] == self._ligand_id
                and pdb["pdbCode"]
            ]
        else:
            return []


    # @ask_about_molecupy
    def all_external_pdbs(self):
        """Queries the RSCB PDB database for PDBs containing this interaction
        by all parameters.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        ligand_external_pdbs = self.ligand().all_external_pdbs()
        target_external_pdbs = self.target().uniprot_pdbs(species=self.species())
        return [code for code in ligand_external_pdbs if code in target_external_pdbs]


    # @ask_about_molecupy
    def all_pdbs(self):
        """Get a list of PDB codes containing this interaction using all means
        available - annotated and external.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        ligand_pdbs = self.ligand().all_pdbs()
        target_pdbs = self.target().all_pdbs(species=self.species())
        return [code for code in ligand_pdbs if code in target_pdbs]


    def species(self):
        """Returns the species in which the interaction takes place.
        :rtype: str"""

        return self._species


    def primary_target(self):
        """Returns ``True`` if the the interaction represents a ligand
        interacting with its primary target.
        :rtype: bool"""

        return self._primary_target


    def endogenous(self):
        """Returns ``True`` if the the interaction is an endogenous interaction.
        :rtype: bool"""

        return self._endogenous


    def interaction_type(self):
        """Returns the type of interaction.
        :rtype: str"""

        return self._interaction_type


    def action(self):
        """Returns the action of the interaction.
        :rtype: str"""

        return self._action


    def affinity_low(self):
        """Returns the lowest reported affinity for this interaction.
        :rtype: float"""

        return self._affinity_low


    def affinity_high(self):
        """Returns the highest reported affinity for this interaction.
        :rtype: float"""

        return self._affinity_high


    def affinity_type(self):
        """Returns the units of the interaction.
        :rtype: str"""

        return self._affinity_type







class Target:
    """A Guide to PHARMACOLOGY target object.
    :param json_data: A dictionary obtained from the web services."""

    def __init__(self, json_data):
        self.json_data = json_data
        self._target_id = json_data["targetId"]
        self._name = json_data["name"]
        self._abbreviation = json_data["abbreviation"]
        self._systematic_name = json_data["systematicName"]
        self._target_type = json_data["type"]
        self._family_ids = json_data["familyIds"]
        self._subunit_ids = json_data["subunitIds"]
        self._complex_ids = json_data["complexIds"]


    def __repr__(self):
        return "<Target %i (%s)>" % (self._target_id, self._name)


    def target_id(self):
        """Returns the target's GtoP ID.
        :rtype: int"""

        return self._target_id


    # @strip_html
    def name(self):
        """Returns the target's name.
        :param bool strip_html: If ``True``, the name will have HTML entities stripped.
        :rtype: str"""

        return self._name


    # @strip_html
    def abbreviation(self):
        """Returns the target's abbreviated name.
        :param bool strip_html: If ``True``, the abbreviation will have HTML entities stripped.
        :rtype: str"""

        return self._abbreviation


    # @strip_html
    def systematic_name(self):
        """Returns the target's systematic name.
        :param bool strip_html: If ``True``, the name will have HTML entities stripped.
        :rtype: str"""

        return self._systematic_name


    def target_type(self):
        """Returns the target's type.
        :rtype: str"""

        return self._target_type


    def family_ids(self):
        """Returns the the family IDs of any families this target is a member of.
        :returns: list of ``int``"""

        return self._family_ids


    def families(self):
        """Returns a list of all target families of which this target is a member.
        :returns: list of :py:class:`TargetFamily` objects"""

        return [get_target_family_by_id(i) for i in self._family_ids]


    def subunit_ids(self):
        """Returns the the target IDs of all targets which are subunits of this
        target.
        :returns: list of ``int``"""

        return self._subunit_ids


    def subunits(self):
        """Returns a list of all targets which are subunits of this target.
        :returns: list of :py:class:`Target` objects"""

        return [get_target_by_id(id_) for id_ in self._subunit_ids]


    def complex_ids(self):
        """Returns the the target IDs of all targets of which this target is a
        subunit.
        :returns: list of ``int``"""

        return self._complex_ids


    def complexes(self):
        """Returns a list of all targets of which this target is a subunit.
        :returns: list of :py:class:`Target` objects"""

        return [get_target_by_id(id_) for id_ in self._complex_ids]


    # @strip_html
    def synonyms(self):
        """Returns any synonyms for this target.
        :param bool strip_html: If ``True``, the synonyms will have HTML entities stripped.
        :returns: list of str"""

        return [synonym["name"] for synonym in self._get_synonym_json()]


    def database_links(self, species=None):
        """Returns any database links for this target.
        :param str species: If given, only links belonging to this species will be returned.
        :returns: list of  :class:`.DatabaseLink` objects."""

        if species:
            return [DatabaseLink(link_json) for link_json in self._get_database_json()
             if link_json["species"] and link_json["species"].lower() == species.lower()]
        else:
            return [DatabaseLink(link_json) for link_json in self._get_database_json()]


    def genes(self, species=None):
        """Returns any genes for this target.
        :param str species: If given, only genes belonging to this species will be returned.
        :returns: list of  :class:`.Gene` objects."""

        if species:
            return [Gene(gene_json) for gene_json in self._get_gene_json()
             if gene_json["species"] and gene_json["species"].lower() == species.lower()]
        else:
            return [Gene(gene_json) for gene_json in self._get_gene_json()]


    def interactions(self, species=None):
        """Returns any interactions for this target.
        :param str species: If given, only interactions belonging to this species will be returned.
        :returns: list of  :class:`.Interaction` objects."""

        if species:
            return [Interaction(interaction_json) for interaction_json in self._get_interactions_json()
             if interaction_json["targetSpecies"] and interaction_json["targetSpecies"].lower() == species.lower()]
        else:
            return [Interaction(interaction_json) for interaction_json in self._get_interactions_json()]


    def get_interaction_by_id(self, interaction_id):
        if not isinstance(interaction_id, int):
            raise TypeError("interaction_id must be int, not '%s'" % str(interaction_id))
        for interaction in self.interactions():
            if interaction.interaction_id() == interaction_id:
                return interaction
        raise NoSuchInteractionError("%s has no interaction %i" % (str(self), interaction_id))

    get_interaction_by_id = get_interaction_by_id
    """Returns an Interaction object of a given ID belonging to the target.
    :param int interaction_id: The interactions's ID.
    :rtype: :py:class:`.Interaction`
    :raises: :class:`.NoSuchInteractionError`: if no such interaction exists in the database."""

    def ask_about_molecupy(func):
        """A decorator which, when applied to a function, will add a 'as_molecupy'
        keyword argument - if set to True this will convert any PDB codes the
        function returns to `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects."""

        def new_func(*args, as_molecupy=False, **kwargs):
            pdbs = func(*args, **kwargs)
            if as_molecupy:
                return [molecupy.get_pdb_remotely(pdb) for pdb in pdbs]
            else:
                return pdbs
        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__
        return new_func

    def ligands(self, species=None):
        """Returns any ligands that this target interacts with.
        :param str species: If given, only ligands belonging to this species will be returned.
        :returns: list of  :class:`.DatabaseLink` objects."""

        ligands = []
        for interaction in self.interactions(species=species):
            ligand = interaction.ligand()
            if ligand not in ligands:
                ligands.append(ligand)
        return ligands


    # @pdb.ask_about_molecupy
    def gtop_pdbs(self, species=None):
        """Returns a list of PDBs which the Guide to PHARMACOLOGY says contain
        this target.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""
        if species is None:
            return [pdb["pdbCode"] for pdb in self._get_pdb_json() if pdb["pdbCode"]]
        else:
            return [pdb["pdbCode"] for pdb in self._get_pdb_json()
             if pdb["pdbCode"] and pdb["species"].lower() == species.lower()]


    # @pdb.ask_about_molecupy
    def uniprot_pdbs(self, species=None):
        """Queries the RSCB PDB database with the targets's uniprot accessions.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :param str species: If given, only PDBs belonging to this species will be returned.
        :returns: list of ``str`` PDB codes"""

        uniprot_accessions = [
         link.accession() for link in self.database_links(species=species)
          if link.database() == "UniProtKB"
        ]
        if uniprot_accessions:
            results = pdb.query_rcsb_advanced("UpAccessionIdQuery", {
             "accessionIdList": ",".join(uniprot_accessions)
            })
            return [result.split(":")[0] for result in results] if results else []
        else:
            return []


    # @pdb.ask_about_molecupy
    def all_pdbs(self, species=None):
        """Get a list of PDB codes using all means available - annotated and
        external.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :param str species: If given, only PDBs belonging to this species will be returned.
        :returns: list of ``str`` PDB codes"""

        return list(set(
         self.gtop_pdbs(species=species) +
         self.uniprot_pdbs(species=species)
        ))


    def _get_synonym_json(self):
        json_object = gtop.get_json_from_gtop(
         "targets/%i/synonyms" % self._target_id
        )
        return json_object if json_object else []


    def _get_database_json(self):
        json_object = gtop.get_json_from_gtop(
         "targets/%i/databaseLinks" % self._target_id
        )
        return json_object if json_object else []


    def _get_gene_json(self):
        json_object = get_json_from_gtop(
         "targets/%i/geneProteinInformation" % self._target_id
        )
        return json_object if json_object else []


    def _get_interactions_json(self):
        json_object = get_json_from_gtop(
         "targets/%i/interactions" % self._target_id
        )
        return json_object if json_object else []


    def _get_pdb_json(self):
        json_object = get_json_from_gtop(
         "targets/%i/pdbStructure" % self._target_id
        )
        return json_object if json_object else []










# start of non libray code
dir_path = os.path.dirname(os.path.realpath(__file__))
AllProtiens = []

with open(dir_path+'/schmidtflynnshererstandard_v4.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        AllProtiens.append(row['symbol_id'])

prot_list = list(set(AllProtiens))

with open(dir_path+'/schmidtflynnsherer_protien_drug_data_v1.csv','w', newline='') as file:
    writer = csv.writer(file)
    count = 0
    writer.writerow(['symbol_id', 'drug_name', 'approved', 'approval_source'])
    for protien in prot_list:
        print(count)
        print(protien)
        count = count + 1
        try:
            target = get_target_by_name(protien)
            # print(target)
            ligand_list = target.ligands()
            if ligand_list != []:

                for ligand in ligand_list:
                    if ligand.approved() == False:
                        writer.writerow((protien, ligand.name(), ligand.approved(), "-"))
                    else:
                        writer.writerow((protien, ligand.name(), ligand.approved(), ligand.approval_source()))
                    # print(ligand.name()," ", ligand.approved(), " ", ligand.approval_source())
            
        except NoSuchTargetError:
            pass