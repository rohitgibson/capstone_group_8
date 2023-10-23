from uuid import uuid4

class SearchComponents:
    def __init__(self) -> None:
        pass

    def searchResults(self, searchResults:list[dict]) -> str:
        """
        Generates a dynamic HTML string containing the search results.

        Args:
            ``searchResults``: 
                A list of search results, each of which is a dictionary.

        Returns:
            A dynamic HTML string containing the search results.
        """

        search_id = str(uuid4())

        # Convert the list of search results into a list of dynamic HTML strings.
        list_search_results = [self.searchResult(searchResult=result["address"], iter=searchResults.index(result), search_id=search_id) for result in searchResults]
        
        # Join the list of dynamic HTML strings into a single string.
        dynamic_search_results = "".join(list_search_results)

        return dynamic_search_results

    def searchResult(self, searchResult:dict, iter:int, search_id:str) -> str:
        """
        Generates a dynamic HTML string containing a single search result.

        Args:
            ``searchResult``: 
                A dictionary containing a single search result.
            ``iter``:
                An integer representing the search result's index
                value in the original list of search results.
            ``search_id``:
                A UUID value assigned to all search results from
                the search request being displayed.

        Returns:
            A dynamic HTML string containing the search result.
        """
        # Extract the address information from the search result.
        searchResult = searchResult["address"]

        # Generate the dynamic HTML string for the search result.
        dynamic_search_result = f"""
            <div class="login-container" id="{search_id}-{iter}">
                
                <div class="result-label">Address Line 1:</div>
                    <div class="result-value">{searchResult["addressLine1"]}</div>
                <div class="result-label">Address Line 2:</div>
                    <div class="result-value">{searchResult["addressLine2"]}</div>
                <div class="result-label">City:</div>
                    <div class="result-value">{searchResult["city"]}</div>
                <div class="result-label">State:</div>
                    <div class="result-value">{searchResult["stateProv"]}</div>
                <div class="result-label">Postal Code:</div>
                    <div class="result-value">{searchResult["postalCode"]}</div>
                <div class="result-label">Country:</div>
                    <div class="result-value">{searchResult["country"]}</div>
            </div>
        """

        return dynamic_search_result