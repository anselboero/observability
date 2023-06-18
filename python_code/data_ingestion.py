import sys
import pandas as pd
# Retrieve information about current user
import getpass
import git

app_user = getpass.getuser()

# Retrieve information about application code from git repo
code_repo = git.Repo(search_parent_directories=True)

# Fetching the latest commit
commit = code_repo.head.commit
code_version = commit.hexsha
code_author = commit.author.name

print(code_repo.is_dirty())

print(code_version, code_author, app_user)




month = sys.argv[1]
year = sys.argv[2]

Apple = pd.read_csv(f"../datasources/{year}/{month}/Apple.csv")
AppTech = pd.read_csv(f"../datasources/{year}/{month}/AppTech.csv")

monthly_asset = pd.concat([Apple, AppTech]).astype({"Symbol": "category"})
monthly_asset.to_csv(f"../datasources/{year}/{month}/monthly_asset.csv", index=False)

