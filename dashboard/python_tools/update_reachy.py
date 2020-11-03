from git import Repo, cmd


def update_reachy():
    local_repo = Repo('/Users/simon/dev/dummy_repo')
    latest_local_tag = str(local_repo.tags[-1])
    
    online_repo_info = cmd.Git().ls_remote('https://github.com/simheo/dummy_repo')
    latest_online_tag = online_repo_info.split('tags/')[-1]

    if latest_online_tag == latest_local_tag:
        print('Reachy is already up-to-date!')
        return

    print('Reachy needs an update.')
    cmd.Git('/Users/simon/dev/dummy_repo').pull()
    print('Reachy is now up-to-date')


if __name__ == "__main__":
    update_reachy()    