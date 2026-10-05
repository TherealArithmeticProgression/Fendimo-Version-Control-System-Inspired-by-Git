<h1>Fendimo</h1>
<a>
<image src='https://github.com/TherealArithmeticProgression/Fendimo-Version-Control-System-Inspired-by-Git/blob/main/image.png', alt='Fendimo Logo'>
</a>

<h2> What is Fendimo?</h2>
As broadly described in the brief description, it's a version control system and it borrows heavily from Git.
Fendimo is content-addressable (address made from the content itself), just like Git. 
<h3>Objects in Fendimo</h3>
Git maintains an active object database for storing various types of "objects" (There are 4 main objects): 

1. Blobs (files)
2. Tree (Directory Structure)
3. Commits (Link to parent tree/commits + metadata about the committer)
4. Annotated Tag (points to a commit and contains tagger notes about the commits)

Fendimo borrows heavily from this structure. If you were to scour Fendimo, you'd find:

1. Blubbers (main objects/files)
2. 

<h3>The .git folder of fendimo</h3>
Git tends to initialize a hidden, safe directory attached directly to the folder (ie, `.git`) and so does fendimo (if you guessed `.fend` you're correct!). The folder con
<h3>The databases inside a `.git` folder</h3>
A `.git` folder attached to the code contains several key subfolders, a few of the prevalent ones include:

`objects/` - The object database. Contains raw file contents, trees and commits compressed using the SHA format.

`refs/` - Contains pointers to commit hashes, arrached i

`info\` - contains global repository information, allowing us to store pivotal information about the repository (such as the files to ignore, stored in the .gitignore file)

`hooks\` - vital automation scripts supported by git, 

`logs\` - history of pointers, helping one mine for previous references
 .
`modules\` - relevant for git submodules
 
`worktrees\` - administrative info on secondary linked working directories

<h2>How is Fendimo any different from Git?</h2>

<h3> It defaults to SHA-256</h3>
Git relies on SHA-1/SHA-1DC to maintain backward compatability, but researchers in the past have successfully demonstrated that SHA-1 can undergo [collision attacks](https://qodex.ai/blog/sha1-vs-sha256). Although Git is actively moving in the forward direction, Fendimo defaults to the SHA-2 (aka, SHA-256) algorithm (SHA-3 would be a better alternative, but SHA-256 is optimized for speed). 


<h2>...And how do you try this out?</h2>
Use these simple steps:

1. Clone the repository: (paste this command in your Git CMD)

```bash
git clone https://github.com/TherealArithmeticProgression/Fendimo-Version-Control-System-Inspired-by-Git
```

2. Then change your working directory
```bash
cd Fendimo-Version-Control-System-Inspired-by-Git
```

3. And run this command in the terminal

```python
pip install -e .
```
(This will install the fendimo package locally)

4. Later, try out the various arguments mentioned in the ARGS.md file. 
(Specimen code)

```python
fendimo make 
```

<h2> Note </h2>
This underlying code was inspired by the code @ [the ugit guide](https://www.leshenko.net/p/ugit/). Create a pullrequest for any suggested changes. Thanks!