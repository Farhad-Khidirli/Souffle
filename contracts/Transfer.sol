// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SendEther {
    constructor() {
    }

    function sendEther(address payable receiver, uint256 amount) public payable {
        require(msg.value >= amount, "Not enough Ether to send");
        receiver.transfer(amount);
    }

    function checkBalance() public view returns (uint256) {
        return address(this).balance;
    }
}




