import pandas as pd
import xml.etree.ElementTree as ET
import json
import os

def read_cat_file(filename):
    """Read the .cat file and return its content"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def register_namespace():
    """Register the BattleScribe namespace"""
    ET.register_namespace('', 'http://www.battlescribe.net/schema/catalogueSchema')
    return {'bs': 'http://www.battlescribe.net/schema/catalogueSchema'}

def create_unit_dataframes(xml_content):
    """Create separate dataframes for different aspects of units"""
    ns = register_namespace()
    root = ET.fromstring(xml_content)
    
    # Main units dataframe
    units_data = []
    weapons_data = []
    profiles_data = []
    abilities_data = []
    vehicles_data = []  # New list for vehicles
    upgrades_data = []
    
    # Look in sharedSelectionEntries and direct selectionEntry for units/vehicles
    entries = root.findall('.//bs:selectionEntry[@type="model"]', namespaces=ns)
    entries.extend(root.findall('.//bs:sharedSelectionEntries//bs:selectionEntry[@type="unit"]', namespaces=ns))
    
    for entry in entries:
        unit_id = entry.get('id')  # Removed trailing comma
        unit_name = entry.get('name')
        
        # Find points cost
        costs = entry.findall('.//bs:cost[@name="pts"]', namespaces=ns)
        if costs and costs[0].get('value'):  # Only process if points exist
            points = costs[0].get('value')
            
            # Check if it's a vehicle by looking at categoryLinks
            categories = [cat.get('name') for cat in entry.findall('.//bs:categoryLink', namespaces=ns)]
            is_vehicle = 'Vehicle' in categories
            
            # Base unit/vehicle data
            base_data = {
                'faction': faction_name,
                'unit_id': unit_id,
                'name': unit_name,
                'points': points,
                'categories': ', '.join(categories)
            }
            
            if is_vehicle:
                vehicles_data.append(base_data)
            else:
                units_data.append(base_data)
            
        # Parse profiles for both units and vehicles
        for profile in entry.findall('.//bs:profile', namespaces=ns):
            profile_type = profile.get('typeName')
            profile_name = profile.get('name')
            
            if profile_type == 'Unit':
                characteristics = {}
                for char in profile.findall('.//bs:characteristic', namespaces=ns):
                    char_name = char.get('name')
                    char_value = char.text
                    characteristics[char_name] = char_value
                
                profile_data = {
                    'faction' : faction_name,
                    'unit_id': unit_id,
                    'name': profile_name,
                    **characteristics
                }
                profiles_data.append(profile_data)
            
            elif profile_type in ['Ranged Weapons', 'Melee Weapons']:
                characteristics = {}
                for char in profile.findall('.//bs:characteristic', namespaces=ns):
                    char_name = char.get('name')
                    char_value = char.text
                    characteristics[char_name] = char_value
                
                weapon_data = {
                    'faction' : faction_name,
                    'unit_id': unit_id,
                    'profile_name': profile_name,
                    **characteristics
                }
                weapons_data.append(weapon_data)
            
            elif profile_type == 'Abilities':
                description = profile.find('.//bs:characteristic', namespaces=ns).text
                ability_data = {
                    'faction' : faction_name,
                    'unit_id': unit_id,
                    'Ability name': profile_name,
                    'Ability Desc.': description
                }
                abilities_data.append(ability_data)
            
            elif profile_type == 'Upgrades':
                upgrades_data.append(ability_data)
    # Create dataframes
    df_units = pd.DataFrame(units_data)
    df_vehicles = pd.DataFrame(vehicles_data)  # New dataframe for vehicles
    df_weapons = pd.DataFrame(weapons_data)
    df_profiles = pd.DataFrame(profiles_data)
    df_abilities = pd.DataFrame(abilities_data)
    df_upgrades = pd.DataFrame(upgrades_data)
    
    return {
        #'faction' : faction_name,
        'units': df_units,
        'vehicles': df_vehicles,  # Added to return dict
        'weapons': df_weapons,
        'profiles': df_profiles,
        'abilities': df_abilities,
        'upgrades' : df_upgrades
    }


def save_dataframes_to_csv(dataframes, output_dir):
    for file in os.listdir(output_dir):
        if file.endswith('.csv'):
            os.remove(os.path.join(output_dir, file))

    for name, df in dataframes.items():
        if isinstance(df, pd.DataFrame) and not df.empty:
            csv_path = f"{output_dir}/{name}.csv"
            df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    cat_file_path = "C:\\stentor\\wh40\\datafiles\\wh40k-10e-main\\Imperium - Black Templars.cat"  # Replace with your actual file path
    faction_name = os.path.basename(cat_file_path).replace('.cat','')
    output_directory =  "C:\\stentor\\wh40\\output" 
   
   
    # Read the file
    xml_content = read_cat_file(cat_file_path)
    
    # Create dataframes
    dataframes = create_unit_dataframes(xml_content)
    save_dataframes_to_csv(dataframes, output_directory)
    
    # Display each dataframe
    for name, df in dataframes.items():
        print(f"\n{name.upper()} DataFrame:")
        print("\nShape:", df.shape)
        print("\nColumns:", df.columns.tolist() if not df.empty else "No columns")
        print("\nContent:")
        pd.reset_option('display.max_rows', None)
        pd.reset_option('display.max_columns', None)
        pd.reset_option('display.width', None)
        print(df)
        print("\n" + "="*80 + "\n")