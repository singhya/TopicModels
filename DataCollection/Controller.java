package nlp_pro;


import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

public class Controller {
	
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		int numberOfCrawlers = 10;
		CrawlConfig config = new CrawlConfig();
		config.setCrawlStorageFolder("E://USC//Sem 2//IR//IR_HW_Workspace//NLP_Crawler//Crawl_Store");
		
		config.setMaxDepthOfCrawling(16);
		config.setMaxPagesToFetch(2000);
		config.setPolitenessDelay(100);
		config.setIncludeBinaryContentInCrawling(true);
		
		PageFetcher pageFetcher = new PageFetcher(config);
		RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
		RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
		CrawlController crController = new CrawlController(config, pageFetcher, robotstxtServer);
		
		crController.addSeed("http://www.amarujala.com/education");
		
		crController.start(Crawler.class, numberOfCrawlers);
	}

}
