This is the repository used to run the automatic tester for ASPECT.

runner.py - this is the main script to run tests and find pull requests
test.sh - this is executed after a revision is checked out and is supposed to run the tests
run.sh/runspecial.sh - wrappers around runner.py for cronjob and manual testing of pull requests
