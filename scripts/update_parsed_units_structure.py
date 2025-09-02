#!/usr/bin/env python3
"""
Update unit_data.json structure to move si_dimension and parsed_dimensions 
from individual units to field level only, removing redundancy.
Also reorders fields so si_dimension and dimensions appear before units.
"""

import json
from pathlib import Path


def update_parsed_units_structure():
    """
    Update the unit_data.json file structure:
    1. Keep si_dimension and parsed_dimensions only at field level (as 'dimensions')
    2. Remove si_dimension, parsed_dimensions, and field from individual units
    3. Add si_dimension at field level if not present
    4. Reorder fields so si_dimension and dimensions appear before units
    """
    
    script_dir = Path(__file__).parent
    input_file = script_dir / "input" / "unit_data.json"
    backup_file = script_dir / "input" / "unit_data.json.backup"
    
    print(f"Reading unit_data.json from: {input_file}")
    
    # Load the current data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create backup
    print(f"Creating backup at: {backup_file}")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Updating structure...")
    updated_count = 0
    
    # Process each field
    for field_name, field_data in data.items():
        if 'units' not in field_data:
            continue
        
        # Get dimensions from first unit (they should all be the same)
        first_unit = field_data['units'][0]
        if 'parsed_dimensions' in first_unit:
            # Ensure field has dimensions
            if 'dimensions' not in field_data:
                field_data['dimensions'] = first_unit['parsed_dimensions']
            
            # Add si_dimension to field level if not present
            if 'si_dimension' not in field_data and 'si_dimension' in first_unit:
                field_data['si_dimension'] = first_unit['si_dimension']
        
        # Remove redundant information from individual units
        for unit in field_data['units']:
            removed_keys = []
            if 'si_dimension' in unit:
                del unit['si_dimension']
                removed_keys.append('si_dimension')
            if 'parsed_dimensions' in unit:
                del unit['parsed_dimensions']
                removed_keys.append('parsed_dimensions')
            if 'field' in unit:
                del unit['field']
                removed_keys.append('field')
            
            if removed_keys:
                updated_count += 1
                print(f"  Removed {removed_keys} from {field_name}.{unit['normalized_name']}")
    
    print(f"Updated {updated_count} units")
    
    # Reorder fields to put si_dimension and dimensions before units
    print("Reordering field properties...")
    reordered_data = {}
    for field_name, field_data in data.items():
        if 'units' not in field_data:
            # Keep non-unit fields as-is
            reordered_data[field_name] = field_data
            continue
        
        # Create new ordered field data
        ordered_field = {}
        
        # Add in desired order: field, normalized_field, si_dimension, dimensions, units
        if 'field' in field_data:
            ordered_field['field'] = field_data['field']
        if 'normalized_field' in field_data:
            ordered_field['normalized_field'] = field_data['normalized_field']
        if 'si_dimension' in field_data:
            ordered_field['si_dimension'] = field_data['si_dimension']
        if 'dimensions' in field_data:
            ordered_field['dimensions'] = field_data['dimensions']
        if 'units' in field_data:
            ordered_field['units'] = field_data['units']
        
        # Add any other fields that might exist
        for key, value in field_data.items():
            if key not in ordered_field:
                ordered_field[key] = value
        
        reordered_data[field_name] = ordered_field
    
    # Replace the original data
    data = reordered_data
    
    # Write the updated data
    print(f"Writing updated data to: {input_file}")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Verify the structure
    print("\nVerifying updated structure...")
    verify_structure(data)
    
    print("✅ Structure update completed successfully!")
    print(f"Backup saved as: {backup_file}")


def verify_structure(data):
    """Verify the updated structure is correct."""
    issues = []
    
    for field_name, field_data in data.items():
        if 'units' not in field_data:
            continue
        
        # Check field level has dimensions
        if 'dimensions' not in field_data:
            issues.append(f"Field '{field_name}' missing dimensions")
        
        # Check units don't have redundant info
        for unit in field_data['units']:
            if 'si_dimension' in unit:
                issues.append(f"Unit '{field_name}.{unit['normalized_name']}' still has si_dimension")
            if 'parsed_dimensions' in unit:
                issues.append(f"Unit '{field_name}.{unit['normalized_name']}' still has parsed_dimensions")
            if 'field' in unit:
                issues.append(f"Unit '{field_name}.{unit['normalized_name']}' still has field")
    
    if issues:
        print("❌ Verification issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Structure verification passed")
        return True


if __name__ == "__main__":
    update_parsed_units_structure()