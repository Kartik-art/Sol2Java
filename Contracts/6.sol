pragma solidity >=0.5.0 <0.6.0;

contract Require {
    // state variables also we can call them storage variables
    address public lawyer;
    
    // after deployment of contract, msg.sender will be lawyer
    constructor() public{
        lawyer = msg.sender;
    }
    
    /**
    * @dev generates random uint256 number
    * 
    * Warning: it isn’t an easy task to generate true random input. 
    * Do not rely on block.timestamp and block.difficulty as a source of randomness. 
    * Since these values can be manipulated by miners.
    * 
    * A good solution includes a combination of several pseudorandom data inputs and
    * the use of oracles or smart contracts to make it more reliable. 
    */
    function idGenerator() external view returns (uint) {
        // the account that invokes this function must be a lawyer
        // otherwise, create an error 'Only lawyer!'
        require(msg.sender == lawyer, 'Only lawyer!');
        
        return uint(keccak256(abi.encode(block.timestamp, block.difficulty)));
    }
    
   function transfer(address payable _to, uint _value) external returns (bool) {
        // _to can't be zero address
        // no error message provided
        // If you do not provide a string argument to require, 
        // it will revert with empty error data
        require(_to != address(0x00));
        
        _to.transfer(_value);
        return true;
    }
}