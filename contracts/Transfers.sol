pragma solidity ^0.8.0;

contract Transfer {

    event ETransfer(address indexed _from, address indexed _to, uint256 _value);

    function transfer(address payable _to) public payable {
        require(msg.value > 0, "Amount must be greater than 0");
        require(address(this).balance >= msg.value, "Insufficient balance");
        _to.transfer(msg.value);
        emit ETransfer(msg.sender, _to, msg.value);
    }

    struct User {
        address publicAddress;
        string encryptedPrivateKey;
        string encryptedPhoneNumber;
        string encryptedEmailAddress;
    }

    mapping(uint256 => User) chatIdToUser;

    function registerUser2(uint256 chatId, address publicAddress, string memory encryptedPrivateKey, string memory encryptedPhoneNumber, string memory encryptedEmailAddress) public {
        User memory newUser = User(publicAddress, encryptedPrivateKey, encryptedPhoneNumber, encryptedEmailAddress);
        chatIdToUser[chatId] = newUser;
    }

    function getUserByChatId(uint256 chatId) public view returns (address, string memory, string memory, string memory) {
        require(chatIdToUser[chatId].publicAddress != address(0), "User not found");
        return (chatIdToUser[chatId].publicAddress, chatIdToUser[chatId].encryptedPrivateKey, chatIdToUser[chatId].encryptedPhoneNumber, chatIdToUser[chatId].encryptedEmailAddress);
    }


}