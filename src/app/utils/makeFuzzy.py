class MakeFuzzy:
    def __init__(self):
        pass

    def execute(self, query_text:str, wildcard_pattern:str):
        """
        Generate a fuzzy search query from a given query 
        text and wildcard pattern.

        Args:
            `query_text`: 
                The query text to fuzzify.
            `wildcard_pattern`: 
                The wildcard pattern to use for fuzzification.

        Returns:
            A string containing the fuzzy search query.
        """
        query_text_list = self.splitQueryText(query_text=query_text)
        fuzzy_query_text_list = self.addFuzzies(query_text_list=query_text_list, wildcard_pattern=wildcard_pattern)
        fuzzy_query_text = self.reassembleQueryTest(fuzzy_query_text_list=fuzzy_query_text_list)

        return fuzzy_query_text

    def splitQueryText(self, query_text:str) -> list:
        """
        Split the query text into a list of words.

        Args:
            `query_text`: 
                The query text to split.

        Returns:
            A list containing the words in the query text.
        """

        # Replace hyphens with spaces to handle hyphenated words.
        if '-' in query_text:
            query_text = query_text.replace("-", r" ")
        else:
            pass

        # Split the query text into individual words.
        query_text_list = query_text.split()

        return query_text_list

    def addFuzzies(self, query_text_list:list, wildcard_pattern:str) -> list:
        """
        Add fuzzy wildcards to each word in the query text list.

        Args:
            `query_text_list`: 
                The query text list to fuzzify.
            `wildcard_pattern`: 
                The wildcard pattern to use for fuzzification.

        Returns:
            A list of words with added wildcards for levenshtein
            distance fuzzy matching via RediSearch.
        """

        # Create a lambda function to apply the wildcard pattern to each word.
        fuzzyLambda = lambda word: rf"{wildcard_pattern}{word}{wildcard_pattern}"

        # Apply the fuzzy lambda function to each word in the query text list.
        fuzzy_query_text_list = list(map(fuzzyLambda, query_text_list))

        return fuzzy_query_text_list

    def reassembleQueryTest(self, fuzzy_query_text_list:list) -> str:
        """Reassemble the fuzzy query text list into a string.

        Args:
            `fuzzy_query_text_list`: 
                A list containing words from the original search
                query with added wildcards.

        Returns:
            The fuzzy search query as a single string.
        """

        # Join the fuzzy words into a single string with spaces between them.
        fuzzy_query_text = " ".join(fuzzy_query_text_list)
        
        return fuzzy_query_text

    