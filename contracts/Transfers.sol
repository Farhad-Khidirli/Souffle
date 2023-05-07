// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Transfer {

    event ETransfer(address indexed _from, address indexed _to, uint256 _value);

    function transfer(address payable _to, bytes32 message_hash, uint8 _v, bytes32 _r, bytes32 _s) public payable {

        require(msg.value > 0, "Amount must be greater than 0");
        require(msg.sender.balance >= msg.value, "Insufficient balance");
        //        bytes32 prefix = "\x19Ethereum Signed Message:\n32";
        //        bytes32 prefixedHash = keccak256(abi.encodePacked(prefix, message_hash));
        address recoveredAddress = ecrecover(message_hash, _v, _r, _s);
        require(recoveredAddress == msg.sender, "Invalid signature");
        _to.transfer(msg.value);
        emit ETransfer(msg.sender, _to, msg.value);
    }

    mapping(uint256 => User) chatIdToUser;

    function ecr(bytes32 msgh, uint8 v, bytes32 r, bytes32 s) public pure
    returns (address sender) {
        return ecrecover(msgh, v, r, s);
    }

    struct User {
        address publicAddress;
        bytes encryptedPrivateKey;
        bytes encryptedPhoneNumber;
        bytes encryptedEmailAddress;
    }

    function registerUser(
        uint256 chatId,
        address publicAddress,
        bytes memory encryptedPrivateKey,
        bytes memory encryptedPhoneNumber,
        bytes memory encryptedEmailAddress
    ) public {
        User memory newUser = User(
            publicAddress,
            encryptedPrivateKey,
            encryptedPhoneNumber,
            encryptedEmailAddress
        );
        chatIdToUser[chatId] = newUser;
    }

    function userExists(uint256 chatId) public view returns (bool) {
        return chatIdToUser[chatId].publicAddress != address(0);
    }

    function getUserByChatId(uint256 chatId) public view returns (address, bytes memory, bytes memory, bytes memory) {
        require(userExists(chatId), "User not found");
        return (chatIdToUser[chatId].publicAddress, bytes(chatIdToUser[chatId].encryptedPrivateKey), bytes(chatIdToUser[chatId].encryptedPhoneNumber), bytes(chatIdToUser[chatId].encryptedEmailAddress));
    }

}