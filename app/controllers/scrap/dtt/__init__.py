from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from cairosvg import svg2png

class DrawingTraceScrap:
    
    
    
    def __init__(self,scrap_code,browser_url,hight,width,leftEndPosition,rightEndPosition,strand="",covered=False,objectsType=""):
        self.hight = hight
        self.width = width
        self.leftEndPosition = leftEndPosition
        self.rightEndPosition = rightEndPosition
        self.strand = strand
        self.covered = covered
        self.objectsType = objectsType
        self.scrap_code = scrap_code
        self.browser_url = browser_url
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--headless")
        self.options.add_argument('--disable-dev-shm-usage')
        self.canvas = self.dtt_canvas()

    def dtt_canvas(self):
        canvas = ""
        driver = webdriver.Chrome(executable_path="app/static/drivers/chromedriver", options = self.options)
        site = "embed/dtt/hight="+str(self.hight)+"&width="+str(self.width)+"&leftEndPosition="+str(self.leftEndPosition)+"&rightEndPosition="+str(self.rightEndPosition)
        driver.get(self.browser_url+site)
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "embed_data")))
            element = driver.find_element(By.ID, "embed_dtt_draw")
            canvas = element.get_attribute("innerHTML")
            #with open('/cache/', 'w', encoding='utf-8') as f:
            #    f.write(canvas)
        except TimeoutException:
            print("Cannot find embedData.")
        finally:
            driver.quit()
        return canvas
    
    def get_dtt_svg(self):
        out = "/tmp/"+self.scrap_code+".png"
        svg2png(bytestring=self.canvas,write_to=out)
        return out
