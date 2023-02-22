pragma solidity ^0.8.0;

contract Transfer {

    event ETransfer(address indexed _from, address indexed _to, uint256 _value);

    function transfer(address payable _to) public payable {
        require(msg.value > 0, "Amount must be greater than 0");
        require(address(this).balance >= msg.value, "Insufficient balance");
        _to.transfer(msg.value);
        emit ETransfer(msg.sender, _to, msg.value);
    }
}