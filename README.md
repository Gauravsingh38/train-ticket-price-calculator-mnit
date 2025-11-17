# train-ticket-price-calculator

## Problem Statement
This module is used to calculate the price of a seat in a train. There are different types of ticket calculations are implemented in this module. The types of tickets are:

1. General Ticket
2. Tatkal Ticket

Pricing strategies are also different for different trains. There 2 types are strategies implemented in this module. The types of strategies are:

1. Fix price between all stations
2. Price based on distance between stations

Though basic implementations are done in this module, it is failing to pass all the tests. There different types of failures in this module
1. Logical errors
2. Syntactical errors, etc.

Your job is to fix all the errors in this module and make the tests pass.

Each test has different points assigned to it. Your final score will be the sum of all the points of the tests that you have passed.


## How to run tests locally
1. install just (https://github.com/casey/just?tab=readme-ov-file#installation)
2. install uv (https://docs.astral.sh/uv/getting-started/installation/)
3. run `just test` to run all tests
4. run `just test -k <test_name>` to run a specific test

## How to submit your solution
1. Create a branch from main branch
2. Make your changes
3. Run all tests locally and make sure they pass
4. Push your changes to your branch in remote
5. Once you push changes to github, tests will run automatically.
6. Based on how many tests are passed and what tests are passed, you will get your score.
7. You can push code as many times as you want. Each time latest score will be updated and will be considered for final score.

## Leaderboard
1. Once the test is done, make sure you push all your changes to github
2. After this, you will *not be able to push any new changes to this branch*
3. Only final scores submitted will be used for leaderboard.
4. After the score, we will update on the final cutoff.
5. Candidates who are above or on the cutoff will be considered for further round
