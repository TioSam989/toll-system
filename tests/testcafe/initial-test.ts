import { Selector } from 'testcafe';

fixture('Toll System Test')
    .page('https://portagens.infraestruturasdeportugal.pt/');

test('Normal trip test', async (t: TestController) => {
    const entryLocation: string = '1250-161';
    const exitLocation: string = '4000-322';
    
    const geocoders = {
        geoArea: Selector('div.leaflet-routing-geocoders'),
        inputEntry: Selector('div.leaflet-routing-geocoders .leaflet-routing-geocoder').nth(0),
        inputExit: Selector('div.leaflet-routing-geocoders .leaflet-routing-geocoder').nth(1)
    };
    
    await t.wait(2000);
    
    await t.typeText(geocoders.inputEntry.find('input'), entryLocation);
    await t.pressKey('enter');
    
    const entryDropdown = Selector('.leaflet-routing-geocoder-result').nth(0);
    if (await entryDropdown.exists) {
        await t.click(entryDropdown);
    }
    
    const exitInput = Selector('.leaflet-routing-geocoder').nth(1).find('input');
    await t.typeText(exitInput, exitLocation);
    await t.pressKey('enter');
    
    const exitDropdown = Selector('.leaflet-routing-geocoder-result').nth(0);
    if (await exitDropdown.exists) {
        await t.click(exitDropdown);
    }
    
    await t.pressKey('enter');
    
    await t.expect(Selector('.leaflet-routing-container').exists).ok('Route not calculated');
    
    await t.takeScreenshot('screenshots/route-calculated.png');
});