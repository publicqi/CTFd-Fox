pragma solidity ^0.4.26;

contract Example {
    mapping (address => bool) isWinner;
    mapping (address => string) winnerMsg;
    function leaveMsg(string message) public{
        require(isWinner[msg.sender])
        winnerMsg[msg.sender] = message;
    }

    function beAWinner() public {
        isWinner[msg.sender] = true;
    }

/*
    function getMyMsg() public view returns (string){
        if (isWinner[msg.sender]){
            return winnerMsg[msg.sender];
        }
        else{
            revert();
        }
    }
*/
}
