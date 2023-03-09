import pandas as pd
import yaml
from tdc.single_pred import ADME

def get_and_transform_data():
    # get raw data
    target_folder = 'CYP_P450_2C19_Inhibition_Veith_et_al'
    target_subfolder = 'CYP2C19_Veith'
    data = ADME(name = target_subfolder)
    fn_data_original = "data_original.csv"
    data.get_data().to_csv(fn_data_original, index=False)
    
    # create dataframe
    df = pd.read_csv(
        fn_data_original,
        delimiter=",",
    )  # not necessary but ensure we can load the saved data
    
    # check if fields are the same
    fields_orig = df.columns.tolist()
    assert fields_orig == ['Drug_ID', 'Drug', 'Y']

    # overwrite column names = fields
    fields_clean = ['chembl_id',
            'SMILES', 
            f"{target_subfolder.split('_')[0]}_inhibition"]
    
    df.columns = fields_clean

#     # data cleaning
#     df[fields_clean[0]] = (
#         df[fields_clean[0]].str.strip()
#     )  
    # remove leading and trailing white space characters
    df = df.dropna()
    assert not df.duplicated().sum()
    
    # save to csv
    fn_data_csv = "data_clean.csv"
    df.to_csv(fn_data_csv, index=False)
    meta = {
        "name": f"{target_folder}",  # unique identifier, we will also use this for directory names
        "description": """The CYP P450 genes are essential in the breakdown (metabolism) of various molecules and chemicals within cells. A drug that can inhibit these enzymes would mean poor metabolism to this drug and other drugs, which could lead to drug-drug interactions and adverse effects. Specifically, the CYP2C19 gene provides instructions for making an enzyme called the endoplasmic reticulum, which is involved in protein processing and transport.""",
        "targets": [
            {
                "id": "CYP2C19_inhibition",  # name of the column in a tabular dataset
                "description": "The ability of the drug to inhibit CYP 2C19 (1) or not (0)",  # description of what this column means
                "units": "active",  # units of the values in this column (leave empty if unitless)
                "type": "categorical",  # can be "categorical", "ordinal", "continuous"
                "names": [  # names for the property (to sample from for building the prompts)
                    "CYP P450 2C19",
                    "CYP 2C19 inhibition",
                    "ADME Drug metabolism",
                    "Pharmacokinetics metabolism",
                    "activity toward CYP2C19",
                ],
                "uris":[
                    "https://bioportal.bioontology.org/ontologies/NCIT?p=classes&conceptid=http%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23C26633",
                    "https://bioportal.bioontology.org/ontologies/NCIT?p=classes&conceptid=http%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23C26512",
                ],
            },
        ],
        "identifiers": [
            {
                "id": "SMILES",  # column name
                "type": "SMILES",  # can be "SMILES", "SELFIES", "IUPAC", "Other"
                "description": "SMILES",  # description (optional, except for "Other")
            },
        ],
        "license": "CC BY 4.0",  # license under which the original dataset was published
        "links": [  # list of relevant links (original dataset, other uses, etc.)
            {
                "url": "https://doi.org/10.1038/nbt.1581",
                "description": "corresponding publication",
            },
            {
                "url": "https://tdcommons.ai/single_pred_tasks/adme/#cyp-p450-2c19-inhibition-veith-et-al",
                "description": "data source",
            }
        ],
        "num_points": len(df),  # number of datapoints in this dataset
        "bibtex": [
            """@article{Veith2009,
          doi = {10.1038/nbt.1581},
          url = {https://doi.org/10.1038/nbt.1581},
          year = {2009},
          month = oct,
          publisher = {Springer Science and Business Media {LLC}},
          volume = {27},
          number = {11},
          pages = {1050--1055},
          author = {Henrike Veith and Noel Southall and Ruili Huang and Tim James and Darren Fayne and Natalia Artemenko and Min Shen and James Inglese and Christopher P Austin and David G Lloyd and Douglas S Auld},
          title = {Comprehensive characterization of cytochrome P450 isozyme selectivity across chemical libraries},
          journal = {Nature Biotechnology}}""",
        ],
    }
    
    def str_presenter(dumper, data):
        """configures yaml for dumping multiline strings
        Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
        """
        if data.count("\n") > 0:  # check for multiline string
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    yaml.add_representer(str, str_presenter)
    yaml.representer.SafeRepresenter.add_representer(
        str, str_presenter
    )  # to use with safe_dum
    fn_meta = "meta.yaml"
    with open(fn_meta, "w") as f:
        yaml.dump(meta, f, sort_keys=False)

    print(f"Finished processing {meta['name']} dataset!")

if __name__ == "__main__":
    get_and_transform_data()
