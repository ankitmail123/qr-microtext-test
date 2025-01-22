export function base64Decode(base64: string): string {
    const buffer = Buffer.from(base64, 'base64');
    return buffer.toString('binary');
}
