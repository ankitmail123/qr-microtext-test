import { readFileSync } from 'fs';
import { detectMicropattern, detectDensityPattern } from './utils/securityAnalyzer';
import { base64Decode } from './utils/base64Utils';

async function runTests() {
    try {
        // Read test cases
        const testCases = JSON.parse(readFileSync('../test_cases.json', 'utf8'));
        
        console.log('\nScanner Security Feature Detection Test Results:');
        console.log('==============================================');
        
        for (const testCase of testCases) {
            console.log(`\nTest Case ${testCase.case_number}:`);
            console.log(`Text: ${testCase.text}`);
            console.log(`Security Code: ${testCase.security_code}`);
            
            // Test standard QR
            console.log('\nTesting Standard QR:');
            const standardMicroResult = await detectMicropattern(testCase.standard_qr, testCase.security_code);
            const standardDensityResult = await detectDensityPattern(testCase.standard_qr, testCase.security_code);
            console.log('- Micropattern detected:', standardMicroResult);
            console.log('- Density pattern detected:', standardDensityResult);
            
            // Test secure QR
            console.log('\nTesting Secure QR:');
            const secureMicroResult = await detectMicropattern(testCase.secure_qr, testCase.security_code);
            const secureDensityResult = await detectDensityPattern(testCase.secure_qr, testCase.security_code);
            console.log('- Micropattern detected:', secureMicroResult);
            console.log('- Density pattern detected:', secureDensityResult);
            
            // Verify results
            const standardCorrect = !standardMicroResult && !standardDensityResult;
            const secureCorrect = secureMicroResult && secureDensityResult;
            
            console.log('\nResults:');
            console.log('- Standard QR (should be false):', standardCorrect ? 'PASS' : 'FAIL');
            console.log('- Secure QR (should be true):', secureCorrect ? 'PASS' : 'FAIL');
        }
        
    } catch (error) {
        console.error('Error running tests:', error);
    }
}

runTests();
