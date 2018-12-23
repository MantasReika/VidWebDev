# VidWebBack

## TODO:

### 1. Figure out how to implement keyword search
### 2. Search by single genre, rating, release 
### 3. research blob decoding

## Basic Git

### Commit changes to your branch
```sh
> git checkout yourBranch
> git pull
> git commit -m 'commit message about changes made'
> git push
```


### How to merge your changes onto master once you have commited and pushed your changes to yourBranch.
```sh
> git checkout yourBranch
> git merge master
```

If there are any conflicts then solve them before proceeding
```sh
> git checkout master
> git merge yourBranch
```

### How to reset uncommited changes in yourBranch.
```sh
> git reset --hard origin/yourBranch
> git pull
```
