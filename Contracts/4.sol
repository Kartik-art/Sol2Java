pragma solidity >=0.4.22 <0.6.0;
contract Register{
address owner;
   constructor() public {
      owner = msg.sender;
   }
   modifier onlyOwner {
      require(msg.sender == owner);
      _;
   }
   modifier costs(uint price) {
      if (msg.value >= price) {
         _;
      }
   }
   mapping (address => bool) registeredAddresses;
   
   
   function register(uint price) public payable costs(price) {
      registeredAddresses[msg.sender] = true;
   }
   
}

contract test{
uint price;
constructor(uint initialPrice) public { price = initialPrice; }
function changePrice(uint _price) public {
      price = _price;
 }
}
