import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.regex.Pattern;

public class EthereumAddress {
    
    private String address;

    // Constructor
    public EthereumAddress(String address) {
        if (!isValidAddress(address)) {
            throw new IllegalArgumentException("Invalid Ethereum address");
        }
        this.address = address;
    }

    // Returns the address
    public String getAddress() {
        return this.address;
    }

    // Ethereum address validation using regex
    public static boolean isValidAddress(String address) {
        // Check if the address is null or does not match the pattern
        if (address == null || !Pattern.matches("^0x[a-fA-F0-9]{40}$", address)) {
            return false;
        }

        // Check if the address matches lower-case or upper-case format (without checksum)
        if (Pattern.matches("^0x[0-9a-f]{40}$", address) || Pattern.matches("^0x[0-9A-F]{40}$", address)) {
            return true;
        }

        // Validate EIP-55 checksum for mixed-case addresses
        return checkEIP55Checksum(address);
    }

    // EIP-55 checksum validation
    private static boolean checkEIP55Checksum(String address) {
        String noPrefixAddress = address.substring(2); // Remove "0x"
        String addressHash = sha3(noPrefixAddress.toLowerCase());

        for (int i = 0; i < 40; i++) {
            char addressChar = noPrefixAddress.charAt(i);
            int hashChar = Integer.parseInt(Character.toString(addressHash.charAt(i)), 16);

            // Check if each letter is correctly case-sensitive as per the EIP-55 checksum
            if ((hashChar > 7 && Character.isLowerCase(addressChar)) || (hashChar <= 7 && Character.isUpperCase(addressChar))) {
                return false;
            }
        }
        return true;
    }

    // SHA-3 (Keccak-256) hashing for address checksum and security
    public static String sha3(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA3-256");
            byte[] hashBytes = digest.digest(input.getBytes());

            // Convert the byte array into a hexadecimal string
            return String.format("%064x", new BigInteger(1, hashBytes));
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA3-256 algorithm not available", e);
        }
    }

    // Normalize an address (lower-case, checksum validation bypass)
    public static String normalizeAddress(String address) {
        if (isValidAddress(address)) {
            return address.toLowerCase();
        } else {
            throw new IllegalArgumentException("Invalid Ethereum address");
        }
    }

    // Main for testing the EthereumAddress class
    public static void main(String[] args) {
        String testAddress = "0x32Be343B94f860124dC4fEe278FDCBD38C102D88";

        // Validate address
        if (EthereumAddress.isValidAddress(testAddress)) {
            System.out.println("Address is valid.");
        } else {
            System.out.println("Address is invalid.");
        }

        // Normalize the address
        System.out.println("Normalized Address: " + EthereumAddress.normalizeAddress(testAddress));

        // Create EthereumAddress object
        EthereumAddress ethAddress = new EthereumAddress(testAddress);
        System.out.println("Ethereum Address: " + ethAddress.getAddress());
    }
}
