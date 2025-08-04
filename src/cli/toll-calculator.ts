#!/usr/bin/env node

import { chromium } from 'playwright';
import { existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

interface TollResult {
    from: string;
    to: string;
    route?: string;
    cost?: string;
    distance?: string;
    error?: string;
    screenshotPath?: string;
}

async function calculateToll(fromAddress: string, toAddress: string): Promise<TollResult> {
    const screenshotsDir = join(process.cwd(), 'screenshots');
    if (!existsSync(screenshotsDir)) {
        mkdirSync(screenshotsDir, { recursive: true });
    }
    
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();
    
    try {
        await page.goto('https://portagens.infraestruturasdeportugal.pt/', { waitUntil: 'networkidle' });
        await page.waitForTimeout(3000);

        const originInput = page.locator('.leaflet-routing-geocoder').nth(0).locator('input');
        await originInput.fill(fromAddress);
        await page.keyboard.press('Enter');
        await page.waitForTimeout(1000);

        const originSuggestion = page.locator('.leaflet-routing-geocoder-result').first();
        if (await originSuggestion.isVisible()) {
            await originSuggestion.click();
        }

        const destInput = page.locator('.leaflet-routing-geocoder').nth(1).locator('input');
        await destInput.fill(toAddress);
        await page.keyboard.press('Enter');
        await page.waitForTimeout(1000);

        const destSuggestion = page.locator('.leaflet-routing-geocoder-result').first();
        if (await destSuggestion.isVisible()) {
            await destSuggestion.click();
        }

        await page.keyboard.press('Enter');
        
        await page.waitForTimeout(5000);

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const screenshotPath = join(screenshotsDir, `toll-${fromAddress.replace(/[^a-zA-Z0-9]/g, '_')}-to-${toAddress.replace(/[^a-zA-Z0-9]/g, '_')}-${timestamp}.png`);
        await page.screenshot({ path: screenshotPath, fullPage: true });

        const routeContainer = page.locator('.leaflet-routing-container');
        if (await routeContainer.isVisible()) {
            const routeText = await routeContainer.textContent() || '';
            
            const costMatch = routeText.match(/(\d+[.,]\d+)\s*€/);
            const distanceMatch = routeText.match(/(\d+[.,]\d+)\s*km/);
            
            return {
                from: fromAddress,
                to: toAddress,
                route: routeText.trim(),
                cost: costMatch ? costMatch[1] + '€' : 'Not found',
                distance: distanceMatch ? distanceMatch[1] + 'km' : 'Not found',
                screenshotPath
            };
        } else {
            return {
                from: fromAddress,
                to: toAddress,
                error: 'Route not calculated',
                screenshotPath
            };
        }
    } catch (error) {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const screenshotPath = join(screenshotsDir, `toll-error-${timestamp}.png`);
        try {
            await page.screenshot({ path: screenshotPath, fullPage: true });
        } catch {}
        
        return {
            from: fromAddress,
            to: toAddress,
            error: `Error: ${error}`,
            screenshotPath
        };
    } finally {
        await browser.close();
    }
}

async function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.log('Usage: npm run toll-calc "Origin Address" "Destination Address"');
        console.log('Example: npm run toll-calc "Lisboa" "Porto"');
        process.exit(1);
    }

    const [fromAddress, toAddress] = args;
    
    console.log('🚗 Calculating toll for trip...');
    console.log(`From: ${fromAddress}`);
    console.log(`To: ${toAddress}`);
    console.log('⏳ Please wait...\n');

    const result = await calculateToll(fromAddress, toAddress);

    if (result.error) {
        console.log('❌ Error:', result.error);
    } else {
        console.log('✅ Trip calculated successfully!');
        console.log(`📍 Route: ${result.from} → ${result.to}`);
        console.log(`💰 Cost: ${result.cost}`);
        console.log(`📏 Distance: ${result.distance}`);
        if (result.route) {
            console.log(`🛣️  Details: ${result.route.substring(0, 200)}...`);
        }
    }
    
    if (result.screenshotPath) {
        console.log(`📸 Screenshot saved: ${result.screenshotPath}`);
    }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    main().catch(console.error);
}