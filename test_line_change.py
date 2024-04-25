import re
from get_function_from_patch import get_patch_obj
import json



def get_line_changes(patch_file_path, sha_id, project_path, project_name=''):
    patch_obj = get_patch_obj(patch_file_path, sha_id, project_path)
    diff_hunk_list = patch_obj.diff_list
    print(diff_hunk_list,patch_obj)
    line_changes = []
    for hunk in diff_hunk_list:
        if hunk.changes:
            changed_file = hunk.old_file_name

            for ch in hunk.changes:
                changed_lines = ch.corres_code
                if changed_lines != None or len(changed_lines) > 0 :
                    for line_pair in changed_lines:
                        line_before_change = line_pair[0]
                        line_after_change = line_pair[1]


                        line_dict = {'project_name': project_name,
                                     "commit_id": sha_id,
                                     "changed_file": changed_file,
                                     "line_before": line_before_change,
                                     "line_after": line_after_change}

                        line_changes.append(line_dict)

    return line_changes



# Example usage:
patch_file_path = ""
# sha_id = "3829759bd042c03225ae862062560f568ba1a231"     # curl
sha_id = "fe4381a658d8f5e151aee0cfe4d9f9734a54a202"

project_path = r"D:\project\func_extract\func_extract\download\variantValidator"
project_name = "curl"
print(get_line_changes(patch_file_path, sha_id, project_path))

# save into csv file using pandas
import pandas as pd
df = pd.DataFrame(get_line_changes(patch_file_path, sha_id, project_path))
df.to_csv('line_changes.csv', index=False)


# save to json file
with open('line_changes.json', 'w') as f:
    json.dump(get_line_changes(patch_file_path, sha_id, project_path), f)
