package nlp_pro;


import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

public class Crawler extends WebCrawler{

	private final static Pattern FILTERS = Pattern.compile(".*((\\.(css|js|mp3|jp?g|png|gif|doc|pdf|zip|gz|json|xml).*)|((urss|xml).*))");
	
	
	public static String wrtFile = "AmarUjala_education.txt";
	public static FileWriter fw;
	public static String fin;
	public static String wrtFile1 = "visit_urls_education.csv";
	public static FileWriter fw1;
	public static String fin1;
	public static int flag =0;
	public static String u ="";
	public static HashSet<String> visit_url;
	public static HashSet<String> all_txt;
	public static ArrayList<String> eng_sen;
	
	@Override
	public boolean shouldVisit(Page page, WebURL url) {
		// TODO Auto-generated method stub
		String href = url.getURL().toLowerCase();
		return !FILTERS.matcher(href).matches()
				&& (href.startsWith("http://www.amarujala.com/education"));
				/*
				|| href.startsWith("http://www.amarujala.com/crime"));
				*/
	}
	
	
	@Override
	public void visit(Page page) {
		// TODO Auto-generated method stub
		
		try{
			fin="";
			if(flag == 0){
				fw = new FileWriter(wrtFile);
				fw1 = new FileWriter(wrtFile1);
				visit_url = new HashSet<String>();
				all_txt = new HashSet<String>();
				eng_sen = new ArrayList<String>();
			}
			flag++;
			synchronized (this) {
				if(page.getParseData() instanceof HtmlParseData){
					HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
					String html = htmlParseData.getHtml();
					String url = page.getWebURL().getURL().toLowerCase();
					//System.out.println("VISIT: "+ url);
					//System.out.println("HTML: "+ html);
					Document doc = Jsoup.parse(html);
					doc.removeClass("twitter-tweet");
					Elements links = doc.select("div");
					Iterator<Element> it = links.iterator();
					
					String text="";
					Element link;
					Elements children;
					while(it.hasNext()){
						link = it.next();
						if(link.attr("class").equals("desc")){
							//System.out.println("Division Class: "+ link.attr("class"));
							//text.replaceAll(",", "(COMMA)");
							
							
							children = link.children();
							if(!children.isEmpty()){
								Iterator<Element> child_it = children.iterator();
								Element child;
								while(child_it.hasNext()){
									child = child_it.next(); 
									if(child.attr("data-lang").equals("en") || child.attr("class").equals("instagram-media") || child.text().contains("Read Also")){
										child.text("");
									}
								}
							}
							if(!text.contains(link.text())){		
								if(!link.text().matches(".*Updated (Mon|Tue|Wed|Thu|Fri|Sat|Sun).*")){
									text += link.text();
									break;
								}
							}
							//System.out.println("Text: "+ text);
						}
						if(link.attr("class").equals("caption")){
							//System.out.println("Division Class: "+ link.attr("class"));
							//text.replaceAll(",", "(COMMA)");
							
							
							children = link.children();
							if(!children.isEmpty()){
								Iterator<Element> child_it = children.iterator();
								Element child;
								while(child_it.hasNext()){
									child = child_it.next(); 
									if(child.attr("data-lang").equals("en") || child.attr("class").equals("instagram-media") || child.text().contains("Read Also")){
										child.text("");
									}
								}
							}
							if(!text.contains(link.text())){		
								if(!link.text().matches(".*Updated (Mon|Tue|Wed|Thu|Fri|Sat|Sun).*")){
									text += link.text();
									break;
								}
							}
							//System.out.println("Text: "+ text);
						}
					}
					if(text != ""){
						if(!visit_url.contains(url) && !all_txt.contains(text)){
							fin = text+"\n";
							fin1 = url+"\n";
							//System.out.println("Text: "+ text);
							//System.out.println("URL: "+ url);
							Files.write(Paths.get(wrtFile), fin.getBytes(), StandardOpenOption.APPEND);
							Files.write(Paths.get(wrtFile1), fin1.getBytes(), StandardOpenOption.APPEND);
							all_txt.add(text);
							visit_url.add(url);
						}
					}
				}
			}
		}catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}

	}
	
}


