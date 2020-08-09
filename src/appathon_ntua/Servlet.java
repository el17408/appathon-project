package appathon_ntua;

import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.util.*;
import java.sql.*;


public class Servlet extends HttpServlet {
	private static final long serialVersionUID = 1L;

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}
	
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {		
		try
		{
			response.setContentType("text/html");
			
			try{
				Class.forName("com.mysql.jdbc.Driver");
				String jdbcUrl = "jdbc:mysql://localhost:3306/internetandapplications";
				String username = "root";
				String password = "";
				Connection connection = null;
				
			    connection = DriverManager.getConnection(jdbcUrl, username, password);
				Statement statement = connection.createStatement();

				String input=request.getParameter("search");
				input = input.replace("+"," ");
				String sql = "SELECT country_name , count(*) as cnt FROM `country` c join `condition` t on c.nct_id = t.nct_id where cond LIKE '%"+input+"%' group by country_name order by cnt DESC";
				ResultSet rs = statement.executeQuery(sql);
				
				String format=request.getParameter("format");
				
				List<String> country = new ArrayList<String>() ;
				List<Integer> counter = new ArrayList<Integer>() ;
				while (rs.next())
				{
					String cntry = rs.getString("country_name");
					
					cntry = cntry.replace(", Republic of","");
					cntry = cntry.replace(", The Democratic Republic of the","");
					cntry = cntry.replace(", Democratic Peoples Republic of","");
					cntry = cntry.replace(", Islamic Republic of","");
					cntry = cntry.replace(", occupied","");
					if( cntry.equals("Togo") || cntry.equals("Georgia")) 
						cntry =cntry + " Country";
					country.add(cntry);
					counter.add(Integer.parseInt(rs.getString("cnt")));
					
				}
				HttpSession session = request.getSession();
				session.setAttribute("countries", country); 
				session.setAttribute("counters", counter);
				session.setAttribute("format", format);
				rs.close();
				statement.close();
				response.sendRedirect("index.jsp");
			}
			catch (ClassNotFoundException e)
			{
				System.out.println(e.getMessage());
			}
		}
		catch (SQLException e)
		{
			throw new RuntimeException("Unable to connect to db, please try again!", e);
		}		
		
	}
	
}