package tests;

import java.time.Duration;

import org.junit.jupiter.api.AfterEach;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import io.github.bonigarcia.wdm.WebDriverManager;

public class ExampleTest {

    private WebDriver driver;
    private WebDriverWait wait;

    // Settings: change these values for your project
    private static final String BASE_URL = "https://www.google.com";        // or your test website
    private static final String EXPECTED_TITLE = "Google";                  // change if using another site
    private static final String SEARCH_QUERY = "Selenium WebDriver";        // any search text

    @BeforeEach
    public void setUp() {
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @Test
    public void testHomePageTitle() {
        driver.get(BASE_URL);
        String actualTitle = driver.getTitle();
        assertEquals(EXPECTED_TITLE, actualTitle, "Title does not match expected.");
    }

    @Test
    public void testSearchFunctionality() {
        driver.get(BASE_URL);

        // Locate the search field (adjust selector for your website)
        WebElement searchInput = driver.findElement(By.cssSelector("input[name='q']"));
        searchInput.sendKeys(SEARCH_QUERY);

        // Locate the search button (adjust selector)
        WebElement searchButton = driver.findElement(By.cssSelector("button[type='submit']"));
        searchButton.click();

        // Wait for the first result to appear (adjust selector)
        WebElement firstResult = wait.until(
            ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".search-result"))
        );
        assertTrue(firstResult.isDisplayed(), "Search result is not visible.");
    }

    @AfterEach
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}