pragma solidity >=0.8.2 <0.8.4;
contract Sample{

function  fun2(uint i, uint j, uint k)
    pure  public  returns(uint){
		k = 0;
		i = 4;
		for(uint i = 0; k<100; ){
			if(j<20){
				j = i;
				k = k + 1;
				k = k + 5;
			}
			else{
				j = k;
				k = k + 2;
				i = 4;
			}
			j = k + j;
			k = i;
		}
		j = i+j;
		return j;
	}
}

