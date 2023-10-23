

class AddComponents:
    def __init__(self) -> None:
        pass

    def addAddressForm(self):
        add_address_form = """
            <div class="login-container">
                <h3 id="titlesmall">Group 8</h3>
                <h1 id="titlebig">Add Address</h1>
                <div class="input-label">
                    <form>
                        <label for="address" class="input-label">Address:</label>
                            <input type="text" id="address" name="address" class="input-field">
                        <label for="address two" class="input-label"></label>
                            <input type="text" id="address two" name="address two" class="input-field">
                        <label for="city" class="input-label">City:</label>
                            <input type="text" id="city" name="city" class="input-field">
                        <label for="state" class="input-label">State:</label>
                            <input type="text" id="state" name="state" class="input-field">
                        <label for="zip" class="input-label">Zip Code:</label>
                            <input type="text" id="zip" name="zip" class="input-field">
                    </form>
                    <a href="Admin-Home.html" class="search-button">Add Address</a>
                </div>
	        </div>
        """

        return add_address_form