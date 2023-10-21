

class SearchComponents:
    def __init__(self) -> None:
        pass

    def searchResults(self, searchResults:list[dict]) -> str:
        listSearchResults = [self.searchResult(searchResult=result["address"]) for result in searchResults]
        dynamicSearchResults = "".join(listSearchResults)

        return dynamicSearchResults

    def searchResult(self, searchResult:dict) -> str:
        dynamicSearchResult = f"""
            <div class="login-container">
                <div class="result-label">Address Line 1:</div>
                    <div class="result-value" id="address">{searchResult["addressLine1"]}</div>
                <div class="result-label">Address Line 2:</div>
                    <div class="result-value" id="address two">{searchResult["addressLine2"]}</div>
                <div class="result-label">City:</div>
                    <div class="result-value" id="city">{searchResult["city"]}</div>
                <div class="result-label">State:</div>
                    <div class="result-value" id="state">{searchResult["stateProv"]}</div>
                <div class="result-label">Postal Code:</div>
                    <div class="result-value" id="postalCode">{searchResult["postalCode"]}</div>
                <div class="result-label">Country:</div>
                    <div class="result-value" id="country">{searchResult["country"]}</div>
            </div>
        """

        return dynamicSearchResult