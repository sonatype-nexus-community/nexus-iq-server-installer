CI with GitHub Actions Notes
================
Tracking the things I did to use and locally run CI builds with GitHub Actions.

* Local build: Use [Nectos/Act](https://github.com/nektos/act) to GitHub Actions locally.

  Some common commands:
  * The command below will look in `.github/workflows` for a `.yml` file containing a `job` with id: `build`, and run that job:

        act -j build

Misc
----

* Setup Branch Protections
  
  see Settings -> Branches -> Branch protection rules -> `main` ->
  
  Under: "Protect matching branches"

  Check: `Require status checks to pass before merging`

  Check: `Require branches to be up to date before merging`

  Under "Status checks that are required.", ensure this line exists: 
  
   `Build Installer` -> "GitHub Actions" 

  Note: `Build Installer` maps directly to the job with that name in the file: [build.yml](./workflows/build.yml).
