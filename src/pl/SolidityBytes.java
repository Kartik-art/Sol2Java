import java.util.Arrays;

public class SolidityBytes {
    
    private byte[] bytes;
    private final int maxSize;
    private final boolean isFixedSize;

    // Constructor for fixed-size byte arrays
    public SolidityBytes(int size) {
        this.maxSize = size;
        this.isFixedSize = true;
        this.bytes = new byte[size];
    }

    // Constructor for dynamic byte arrays
    public SolidityBytes() {
        this.maxSize = Integer.MAX_VALUE;
        this.isFixedSize = false;
        this.bytes = new byte[0];
    }

    // Constructor to initialize from an existing byte array
    public SolidityBytes(byte[] bytes, boolean isFixedSize) {
        this.bytes = Arrays.copyOf(bytes, bytes.length);
        this.isFixedSize = isFixedSize;
        this.maxSize = isFixedSize ? bytes.length : Integer.MAX_VALUE;
    }

    // Getter to retrieve the bytes
    public byte[] getBytes() {
        return Arrays.copyOf(bytes, bytes.length);
    }

    // Method to set bytes, enforcing length constraints if fixed-size
    public void setBytes(byte[] newBytes) {
        if (newBytes.length > maxSize) {
            throw new IllegalArgumentException("Byte array exceeds maximum allowed size.");
        }
        this.bytes = Arrays.copyOf(newBytes, newBytes.length);
    }

    // Method to slice the byte array
    public SolidityBytes slice(int start, int end) {
        if (start < 0 || end > bytes.length || start > end) {
            throw new IndexOutOfBoundsException("Invalid slice indices.");
        }
        return new SolidityBytes(Arrays.copyOfRange(this.bytes, start, end), false);
    }

    // Method to concatenate two SolidityBytes arrays
    public static SolidityBytes concat(SolidityBytes a, SolidityBytes b) {
        byte[] result = new byte[a.bytes.length + b.bytes.length];
        System.arraycopy(a.bytes, 0, result, 0, a.bytes.length);
        System.arraycopy(b.bytes, 0, result, a.bytes.length, b.bytes.length);
        return new SolidityBytes(result, false);
    }

    // Method for ABI encoding (simplified for demonstration)
    public byte[] encode() {
        // Example encoding rule: prepend with length for dynamic arrays
        if (!isFixedSize) {
            byte[] lengthPrefix = intToBytes(bytes.length);
            byte[] encoded = new byte[lengthPrefix.length + bytes.length];
            System.arraycopy(lengthPrefix, 0, encoded, 0, lengthPrefix.length);
            System.arraycopy(bytes, 0, encoded, lengthPrefix.length, bytes.length);
            return encoded;
        }
        // For fixed size, return bytes directly
        return Arrays.copyOf(bytes, bytes.length);
    }

    // Method for ABI decoding (simplified for demonstration)
    public static SolidityBytes decode(byte[] encodedData, boolean isFixedSize) {
        if (!isFixedSize) {
            int length = bytesToInt(Arrays.copyOfRange(encodedData, 0, 4));
            return new SolidityBytes(Arrays.copyOfRange(encodedData, 4, 4 + length), false);
        } else {
            return new SolidityBytes(encodedData, true);
        }
    }

    // Helper method to convert int to byte array (used for encoding length)
    private static byte[] intToBytes(int value) {
        return new byte[] {
            (byte) (value >> 24),
            (byte) (value >> 16),
            (byte) (value >> 8),
            (byte) value
        };
    }

    // Helper method to convert byte array to int (used for decoding length)
    private static int bytesToInt(byte[] bytes) {
        return (bytes[0] & 0xFF) << 24 |
               (bytes[1] & 0xFF) << 16 |
               (bytes[2] & 0xFF) << 8 |
               (bytes[3] & 0xFF);
    }

    // Additional utility methods for Solidity-like behavior
    public int length() {
        return this.bytes.length;
    }

    public boolean isFixedSize() {
        return this.isFixedSize;
    }

    // Override toString for easier debugging
    @Override
    public String toString() {
        return "SolidityBytes{" +
                "bytes=" + Arrays.toString(bytes) +
                ", maxSize=" + maxSize +
                ", isFixedSize=" + isFixedSize +
                '}';
    }
}
