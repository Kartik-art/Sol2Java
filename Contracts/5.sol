// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

contract A {
    function f(uint value) public pure returns (uint out) {
       for(;value>89;value+9)
		value+=1;  
	 //while(value<4)
	  //	value+=1;
		//do
		//value+=4;
		//while(value<5);
	   
    }

    function f(uint value, bool really) public pure returns (uint out) {
		//for(45;value>45;67)
		//	value+=45;

        if (true)
            out = value;

	   if (value > 456){
		  value += 500;
	   }
    }
}