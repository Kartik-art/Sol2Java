import java.math.BigInteger;

public class SolidityUint {
    private BigInteger value;
    private final BigInteger maxValue;
    private final int bitLength;

    // Constructor to initialize a SolidityUint with a specific number of bits (e.g., 256 for uint256)
    public SolidityUint(BigInteger value, int bits) {
        this.maxValue = BigInteger.TWO.pow(bits).subtract(BigInteger.ONE); // max value based on bits
        this.bitLength = bits;  // Cache the bit length
        
        // Checking if the value is within the range of uint(bits)
        if (value.compareTo(BigInteger.ZERO) < 0 || value.compareTo(this.maxValue) > 0) {
            throw new IllegalArgumentException("Value out of range for uint" + bits);
        }
        this.value = value;
    }

    // Getter for the current value
    public BigInteger getValue() {
        return this.value;
    }

    // Method for addition with overflow protection (modular arithmetic)
    public SolidityUint add(SolidityUint other) {
        BigInteger result = this.value.add(other.value);
        result = result.mod(this.maxValue.add(BigInteger.ONE));  // Use modular arithmetic
        return new SolidityUint(result, this.bitLength);
    }

    // Method for subtraction with underflow protection (wrap around like Solidity)
    public SolidityUint subtract(SolidityUint other) {
        BigInteger result = this.value.subtract(other.value);
        if (result.compareTo(BigInteger.ZERO) < 0) {
            result = result.add(this.maxValue).add(BigInteger.ONE); // Wrap around
        }
        return new SolidityUint(result, this.bitLength);
    }

    // Method for multiplication with overflow protection using modular arithmetic
    public SolidityUint multiply(SolidityUint other) {
        BigInteger result = this.value.multiply(other.value);
        result = result.mod(this.maxValue.add(BigInteger.ONE));  // Proper modular arithmetic
        return new SolidityUint(result, this.bitLength);
    }

    // Method for division (no overflow risk, but handle division by zero)
    public SolidityUint divide(SolidityUint other) {
        if (other.value.equals(BigInteger.ZERO)) {
            throw new ArithmeticException("Division by zero");
        }
        BigInteger result = this.value.divide(other.value);
        return new SolidityUint(result, this.bitLength);
    }

    // Method for modulus operation
    public SolidityUint mod(SolidityUint other) {
        if (other.value.equals(BigInteger.ZERO)) {
            throw new ArithmeticException("Modulus by zero");
        }
        BigInteger result = this.value.mod(other.value);
        return new SolidityUint(result, this.bitLength);
    }

    // Method for bitwise AND operation
    public SolidityUint and(SolidityUint other) {
        BigInteger result = this.value.and(other.value);
        return new SolidityUint(result, this.bitLength);
    }

    // Method for bitwise OR operation
    public SolidityUint or(SolidityUint other) {
        BigInteger result = this.value.or(other.value);
        return new SolidityUint(result, this.bitLength);
    }

    // Method for bitwise XOR operation
    public SolidityUint xor(SolidityUint other) {
        BigInteger result = this.value.xor(other.value);
        return new SolidityUint(result, this.bitLength);
    }

    // Method for checking equality
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        SolidityUint other = (SolidityUint) obj;
        return this.value.equals(other.value);
    }

    // Method to convert the SolidityUint to a string representation (for printing or logging)
    @Override
    public String toString() {
        return "SolidityUint{" + "value=" + value + ", maxValue=" + maxValue + '}';
    }
}
