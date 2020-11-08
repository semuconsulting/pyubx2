# How to contribute

Here are some guidelines on how to contribute to the pyubx2 project.

We appreciate any contribution, from fixing a grammar mistake in a comment to implementing complex algorithms. Please read this section if you are contributing your work.

Being one of our contributors, you agree and confirm that:

* You did your own work.
* Your work will be distributed under a BSD 3-Clause License once your pull request is merged.
* You submitted work fulfils or mostly fulfils our styles and standards.

Please help us keep our issue list small by adding fixes: #{$ISSUE_NO} to the commit message of pull requests that resolve open issues. GitHub will use this tag to auto close the issue when the PR is merged.

## Testing

We use python's native unittest framework for local unit testing, complemented by the Travis CI automated build and testing workflow. We endeavour to have 100% code coverage.

Please write unittest examples for new code you create and add them to the /tests folder following the naming convention test_*.py.

We test on the following platforms using u-blox NEO-6, NEO-7 and NEO-8 devices:
* Windows 10
* MacOS (10.15.7 Catalina)
* Linux (Ubuntu 18, 19, 20)
* Raspberry Pi OS (32-bit)

## Submitting changes

Please send a [GitHub Pull Request to SEMU Consulting](https://github.com/semuconsulting/pyubx2/pulls) with a clear list of what you've done (read more about [pull requests](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-pull-requests)). We can always use more test coverage. Please follow our coding conventions (below) and make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."

## Coding conventions

  * We use Eclipse PyDev for development and testing, but you are at liberty to use your preferred IDE.
  * We use pylint (>=2.6.0) for code analysis.
  * we use black (>= 20.8) for code formatting.
  * We indent using four spaces.
  * We ALWAYS put spaces after list items and method parameters (`[1, 2, 3]`, not `[1,2,3]`), around operators (`x += 1`, not `x+=1`), and around hash arrows.
  * This is open source software. We endeavour to make the code as transparent as possible.

Thanks,

SEMU Consulting