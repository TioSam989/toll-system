#!/usr/bin/env node

import { chromium } from 'playwright';

interface TollResult {
    from: string;
    to: string;
    route?: string;
    cost?: string;
    distance?: string;
    error?: string;
}

async function calculateToll(fromAddress: string, toAddress: string): Promise<TollResult> {
    const browser = await chromium.launch({ headless: true });
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

        await page.waitForTimeout(3000);

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
                distance: distanceMatch ? distanceMatch[1] + 'km' : 'Not found'
            };
        } else {
            return {
                from: fromAddress,
                to: toAddress,
                error: 'Route not calculated'
            };
        }
    } catch (error) {
        return {
            from: fromAddress,
            to: toAddress,
            error: `Error: ${error}`
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
}

if (require.main === module) {
    main().catch(console.error);
}