export type SanitizationStatus = 'applied' | 'skipped';

export interface SanitizationTrace {
    version: string;
    status: SanitizationStatus;
    appliedAt: string;
}

const SANITIZATION_VERSION = '1.0.0';

const stripDangerousTags = (input: string) =>
    input
        .replace(/<script[\s\S]*?>[\s\S]*?<\/script>/gi, '')
        .replace(/<style[\s\S]*?>[\s\S]*?<\/style>/gi, '')
        .replace(/on\w+="[^"]*"/gi, '');

export const sanitizeText = (input: string): string => {
    if (!input) return input;
    return stripDangerousTags(input);
};

export const buildSanitizationTrace = (): SanitizationTrace => ({
    version: SANITIZATION_VERSION,
    status: 'applied',
    appliedAt: new Date().toISOString(),
});
