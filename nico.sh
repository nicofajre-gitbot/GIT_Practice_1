echo "# GIT_Practice_1" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/nicofajre-gitbot/GIT_Practice_1.git
git push -u origin main

#Setting up Git user information for this repository
git config --global user.name "nicofajre-gitbot"
git config --global user.email "nicofajre@gmail.com"
# Treat divergence in Git
git config pull.rebase false #merge (the default strategy)