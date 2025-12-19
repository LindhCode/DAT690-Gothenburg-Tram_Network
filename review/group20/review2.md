Lab 3 peer review

    Reviewing group number: 20
    Submitting group number: 2

# Section 1: Core functionality

    Does the application run? (yes/no)

yes

    Does the application display the complete map of tram lines? (yes/no)

yes

    Is it possible to query shortest path between any two points? (yes/no)

yes

    Does the application deal with changes correctly? (yes/no)

yes

    Does the application show current traffic information? (yes/no)

yes

    Does the application correctly handle invalid input? (yes/no)

yes
# Section 2: Code quality
Make comments on the overall code quality of the submission, including whether:

    code from lab 2 has been properly reused (i.e. in an efficient way without boilerplate code) (utan repetition)

The overall code quality is good and shows clear reuse of code from Lab 2 without unnecessary repetition. The graph and tram data are reused in a reasonable way, and edge cases such as extreme positions are handled according to the instructions. The tramviz code is not directly reused, but this is acceptable. Some visualization functions, such as view_shortest and demo, may be unnecessary since similar functionality could already be handled by show_shortest, and the code could be simplified here.

    the dijkstra() function has been implemented and used as intended: there is just one definition of the function itself, and different distances are obtained by just changing the cost function


The dijkstra() function is implemented correctly and reused in a clean way. There is only one definition of the algorithm, and different distances are calculated by changing the cost function. This makes the code flexible, clear, and easy to maintain.
You may add any other comments about code quality you wish, for example suggestions for code optimization and good practices of object-oriented programming.
As a possible improvement, the visualization could include clearer headings, such as labeling results as “Shortest” and “Quickest.” Showing units like kilometers and minutes would make the output easier to understand. Adding a few short comments or visual separators could also help structure the visualization and improve readability.