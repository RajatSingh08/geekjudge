'''
List of Views:
- AUTHENTICATION: Sign Up/Sign In (will add at the end).
- HOME PAGE: Has a list of problems and filters to sort them on the basis of solved status or difficulty.
- PROBLEM DETAIL: Once a problem is selected, user will be redirected to this page 
                  which has problem details, programming language selection drop-down menu, code submit button.
- VERDICT PAGE: Once the code is submitted, user will be redirected to this page which will show the verdict 
                and first point of difference is output is wrong.
- SUBMISSIONS: To view all the submissions made by that user.
- LEADERBOARD: Diplay the leaderboard.
'''

from django.shortcuts import render
