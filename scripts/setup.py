from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import sys

def configure_tplink_router(retry_count=0, max_retries=2):
    wd_number = ""
    while not wd_number.isdigit():
        wd_number = input("Please enter the PPPoE WD number (digits only, e.g., 1234): ").strip()
        if not wd_number.isdigit():
            print("Invalid input. Please enter only digits for the WD number.")

    pppoe_username = f"WD{wd_number}"
    pppoe_password = f"WD{wd_number}"
    print(f"\nConfiguring with PPPoE Username: {pppoe_username}, Password: {pppoe_password}")

    router_url = "http://192.168.0.1"
    initial_router_password = "C4tM0u3ED@g!"

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except WebDriverException as e:
        print(f"Error initializing ChromeDriver: {e}")
        sys.exit(1)

    try:
        print("Starting router configuration process...")
        driver.get(router_url)
        wait = WebDriverWait(driver, 20)  # Increased timeout from 15 to 20 seconds

        # Initial password setup
        print("Waiting for the initial router password setup page to load...")
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h3[@class='panel-title']/span[@class='panel-title-text' and text()='Create an administrator password']")
        ))

        new_password_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="password" and contains(@class, "password-hidden")]'))
        )
        new_password_field.click()
        new_password_field.send_keys(initial_router_password)

        confirm_password_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='confirm-pwd-tb']//input[contains(@type,'password')]"))
        )
        confirm_password_field.click()
        confirm_password_field.send_keys(initial_router_password)

        lets_get_started_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='local-login-button']/div[2]/div[1]/a"))
        )
        lets_get_started_button.click()
        print("Clicked 'Let's Get Started' button.")
        time.sleep(5)

        # Time zone NEXT
        print("Waiting for NEXT button on Time Zone page...")
        next_button_timezone = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'NEXT')]"))
        )
        next_button_timezone.click()
        print("Clicked NEXT button on Time Zone page.")
        time.sleep(2)

        # Select PPPoE
        print("Selecting PPPoE connection type...")
        pppoe_option = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "ul li:nth-child(3) label span.icon"))
        )
        pppoe_option.click()
        print("Selected PPPoE.")

        # NEXT on connection type page
        print("Waiting for NEXT button on connection type page...")
        next_btn_conn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="qs-choose-internet-type-next-btn"]/div[2]/div[1]/a'))
        )
        try:
            next_btn_conn.click()
            print("Clicked NEXT on connection type page.")
        except Exception:
            driver.execute_script("arguments[0].click();", next_btn_conn)
            print("Clicked NEXT on connection type page via JS.")

        # PPPoE credentials
        print("Waiting for PPPoE credentials fields...")
        time.sleep(2)
        username_input = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[@widget='textbox' and @data-bind='{wanPPPOEModel.username}']//input[@type='text']"
            ))
        )
        username_input.clear()
        username_input.send_keys(pppoe_username)
        print(f"Entered PPPoE username: {pppoe_username}")

        # Add 2 seconds delay before entering password
        print("Waiting 2 seconds before entering password...")
        time.sleep(2)

        password_input = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//input[@type='password' and contains(@class, 'password-hidden')]"
            ))
        )
        password_input.clear()
        password_input.send_keys(pppoe_password)
        print("Entered PPPoE password.")
        time.sleep(2)

        # NEXT on PPPoE page
        print("Waiting for NEXT button on PPPoE credentials page...")
        next_btn_pppoe = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                "#qs-internet-edit-next-step-btn > div.widget-wrap-outer.button-wrap-outer > div.widget-wrap.button-wrap > a"
            ))
        )
        try:
            next_btn_pppoe.click()
            print("Clicked NEXT on PPPoE credentials page.")
        except Exception as e:
            print(f"Regular click failed: {e}, trying JavaScript click...")
            driver.execute_script("arguments[0].click();", next_btn_pppoe)
            print("Clicked NEXT on PPPoE credentials page via JS.")
        time.sleep(5)

        # Wait for wireless wizard to load - Enhanced wait
        print("Waiting for wireless wizard to load...")
        time.sleep(8)  # Increased from 5 to 8 seconds

        # Configure 2.4GHz SSID
        print("Configuring 2.4GHz wireless settings...")
        ssid_2_4g_input = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[@class='container widget-container text-container' and @data-bind='{wirelessQsModel.ssid}']//input[@type='text']"
            ))
        )
        ssid_2_4g_input.clear()
        ssid_2_4g_input.send_keys("Wifi Dabba")
        print("Entered 2.4GHz SSID: Wifi Dabba")

        # Configure 2.4GHz Password
        password_2_4g_input = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[@class='container widget-container text-container' and @data-bind='{wirelessQsModel.password}']//input[@type='text']"
            ))
        )
        password_2_4g_input.clear()
        password_2_4g_input.send_keys("wifidabba")
        print("Entered 2.4GHz password: wifidabba")

        # Configure 5GHz SSID - Enhanced with multiple approaches
        print("Configuring 5GHz wireless settings...")
        
        # Try multiple selectors for 5GHz SSID field
        ssid_5g_selectors = [
            "//div[@class='container widget-container text-container' and @data-bind='{wirelessQsModel5g.ssid}']//input[@type='text']",
            "//div[contains(@data-bind, 'wirelessQsModel5g.ssid')]//input[@type='text']",
            "//div[contains(@data-bind, '5g.ssid')]//input[@type='text']",
            "//input[contains(@data-bind, '5g.ssid')]",
            "(//input[@type='text'])[4]",  # Sometimes it's the 4th text input
            "(//input[@type='text'])[5]"   # Or the 5th text input
        ]
        
        ssid_5g_configured = False
        for selector in ssid_5g_selectors:
            try:
                print(f"Trying 5GHz SSID selector: {selector}")
                ssid_5g_input = wait.until(
                    EC.visibility_of_element_located((By.XPATH, selector))
                )
                ssid_5g_input.clear()
                ssid_5g_input.send_keys("Wifi Dabba")
                print("Entered 5GHz SSID: Wifi Dabba")
                ssid_5g_configured = True
                break
            except Exception as e:
                print(f"5GHz SSID selector failed: {selector} - {e}")
                continue
        
        if not ssid_5g_configured:
            print("Warning: Could not configure 5GHz SSID, continuing with 2.4GHz only...")
            # Take a screenshot for debugging
            driver.save_screenshot(f"5ghz_config_failed_{retry_count}.png")
            print(f"Screenshot saved as 5ghz_config_failed_{retry_count}.png")

        # Wait 10 seconds as requested
        print("Waiting 10 seconds before proceeding...")
        time.sleep(10)

        # Click NEXT button on wireless configuration page
        print("Clicking NEXT button on wireless configuration page...")
        next_btn_wireless = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="qs-wireless-next-step-btn"]/div[2]/div[1]/a'))
        )
        try:
            next_btn_wireless.click()
            print("Clicked NEXT on wireless configuration page.")
        except Exception as e:
            print(f"Regular click failed: {e}, trying JavaScript click...")
            driver.execute_script("arguments[0].click();", next_btn_wireless)
            print("Clicked NEXT on wireless configuration page via JS.")

        # Wait for next wizard to load
        print("Waiting for next wizard to load...")
        time.sleep(3)

        # Click Skip option - Using JavaScript approach (most reliable)
        print("Clicking Skip option...")
        try:
            # Use JavaScript to find and click the Skip option
            driver.execute_script("""
                var skipElements = document.querySelectorAll('input[data-text="Skip"], label[class*="radio-label"]');
                for (var i = 0; i < skipElements.length; i++) {
                    if (skipElements[i].textContent.includes('Skip') || skipElements[i].getAttribute('data-text') === 'Skip') {
                        skipElements[i].click();
                        break;
                    }
                }
            """)
            print("Clicked Skip option via JavaScript.")
        except Exception as e:
            print(f"JavaScript Skip click failed: {e}")

        # Wait for NEXT button to be highlighted/enabled after Skip selection
        print("Waiting for final NEXT button to be enabled...")
        time.sleep(2)

        # Click final NEXT button - Using the working selector
        print("Clicking final NEXT button...")
        try:
            final_next_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="qs-auto-update-next-step-btn"]/div[2]/div[1]/a'))
            )
            final_next_btn.click()
            print("Successfully clicked final NEXT button.")
        except Exception as e:
            print(f"Regular click failed: {e}, trying JavaScript click...")
            try:
                final_next_btn = driver.find_element(By.XPATH, '//*[@id="qs-auto-update-next-step-btn"]/div[2]/div[1]/a')
                driver.execute_script("arguments[0].click();", final_next_btn)
                print("Successfully clicked final NEXT button via JavaScript.")
            except Exception as js_e:
                print(f"JavaScript click also failed: {js_e}")

        # Wait a moment for configuration to complete
        time.sleep(3)

        print("=" * 60)
        print("🎉 TP-Link Router Configuration Completed Successfully! 🎉")
        print("=" * 60)
        print("Configuration Summary:")
        print(f"✓ PPPoE Username: {pppoe_username}")
        print(f"✓ PPPoE Password: {pppoe_password}")
        print("✓ 2.4GHz SSID: Wifi Dabba")
        print("✓ 5GHz SSID: Wifi Dabba")
        print("✓ WiFi Password: wifidabba")
        print("✓ Auto-update: Skipped")
        print("=" * 60)
        print("Your router is now ready to use!")

    except TimeoutException as e:
        print(f"Timeout error: {e}")
        print("Taking screenshot for debugging...")
        driver.save_screenshot(f"error_screenshot_attempt_{retry_count}.png")
        
        # If we haven't reached max retries, try again
        if retry_count < max_retries:
            print(f"\n{'='*60}")
            print(f"⚠️  ATTEMPT {retry_count + 1} FAILED - RETRYING...")
            print(f"{'='*60}")
            driver.quit()
            time.sleep(5)  # Wait before retry
            return configure_tplink_router(retry_count + 1, max_retries)
        else:
            print(f"\n{'='*60}")
            print("❌ CONFIGURATION FAILED AFTER ALL RETRIES")
            print(f"{'='*60}")
            print("Please check the screenshots for debugging information.")
            print("You may need to manually reset the router and try again.")
            
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
        if retry_count < max_retries:
            print(f"Retrying... (Attempt {retry_count + 2})")
            driver.quit()
            time.sleep(5)
            return configure_tplink_router(retry_count + 1, max_retries)
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if retry_count < max_retries:
            print(f"Retrying... (Attempt {retry_count + 2})")
            driver.quit() 
            time.sleep(5)
            return configure_tplink_router(retry_count + 1, max_retries)
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    configure_tplink_router()%                                        
