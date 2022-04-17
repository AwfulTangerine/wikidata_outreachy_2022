## Introduction
Here stores my contributions (currently task 3) around Wikidata's project #4:
_"What's in a name? Automatically identifying first and last author names for Wikicite and Wikidata"._


If there are any issues or new features to be developed, we can discuss through my usertalk (https://www.wikidata.org/wiki/User_talk:Jiehui_Ma) /  pull issues directly in this repository / send messages via other channels:
- Zulip message & Email: awfultangerine@gmail.com
- Linkedin: https://www.linkedin.com/in/jiehuima/


## Task 3 contributions
For this task (https://phabricator.wikimedia.org/T301737), I designed functions to:
- Automatically get bibcode for astronomical scientific articles;
  - If the 'ADS bibcode' identifier already on item page, generate urls based on the bibcode;
  - If no identifier, will redirect to search bibcode via ADS's official website & add identifiers for the article item page.
- Clean raw bibcode texts to get author information (& topics);
- Match author info in bibcode & on wikidata item page;
- Add relevant qualifiers to detect first and last names.

Through this script, we can detect author first & last names based on BiBTeX information, by simply inputting the Q number of article item pages. Besides https://ui.adsabs.harvard.edu/abs/2014A%26A...569A..59I/abstract, I tested in 8 extra astronomical articles and the script works fine.


## My trials to realize this contribution
While working on task 3, I have tried various methods to realize different parts of this task.
- The methods I tried for fetching the bibcodes include: 
    - Beautiful Soup + str.split(): The method I eventually used in current script. It was too fragile to be maintained, possibly break down and not easy to identify the faults, if error occured.
    - Regular Expressions: The method I've tried to learn, but due to the complexity of the bibcode text, it is also not easy to maintain and detect errors. However, comparing to split(), it is more Pythonic.
    - Other Python libs - bibtexparser (https://bibtexparser.readthedocs.io) and parse: The disadvantages are the same as the other two methods. PS: the libraries are not used by many people in these days, so we might face unexpected errors.
- However, after seeing articles in other fields, I realized not all articles have the same format. The most obvious differences include:
    -  The first & last names might not be in the same order.
    -  Some are listed in full names while others have their first / last names abbreviated.
    -  Some may put last names in {} while others do not.
    -  The amount & position of spaces and line breaks might also be different.
I would like to further discuss with you and search for new methods to deal with the complex and not-that-structurized bibcodes.

