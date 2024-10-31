pragma solidity >=0.5.2 <0.5.11;
contract Sample{

function  fun2(uint i, uint j, uint k)
    pure  public  returns(uint){
		assert(1 wei == 1);
assert(1 szabo == 1e12);
assert(1 finney == 1e15);
assert(1 ether == 1e18);
assert(2 ether == 2000);
assert(1 seconds == 1);
assert(1 minutes == 60 seconds);
assert(1 hours == 60 minutes);
}
}
contract LedgerBalance {
   mapping(address => uint) public balances;

   function updateBalance(uint newBalance) public {
      balances[msg.sender] = newBalance;
   }
}
contract Updater {
   function updateBalance() public returns (uint) {
      LedgerBalance ledgerBalance = new LedgerBalance();
      ledgerBalance.updateBalance(10);
      return ledgerBalance.balances(address(this));
   }
function f(uint start, uint daysAfter) public {
    if (now >= start + daysAfter * 1 days) {
		uint now = now;
		start += 360 + now;
    }
}
}
