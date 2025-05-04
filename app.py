import streamlit as st
from g4f.client import Client
import base64
from io import BytesIO
import requests
from datetime import datetime
import os

# Initialize the client
client = Client()

# App title and layout
st.set_page_config(page_title="AI House Plan Generator", layout="wide")
st.title("🏡 Ai Architectural Assistant")
st.write("Describe your ideal home and get a professional-style floor plan with labeled dimensions.")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Generate Plan", "My Saved Plans", "Help & Tips"])

with tab1:
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📐 House Specifications")
        
        # City selection
        tamilnadu_cities = [
            "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Tiruppur", "Vellore", "Thoothukudi", "Erode"
        ]
        selected_city = st.selectbox("Choose Location (Top 10 Cities in Tamil Nadu)", tamilnadu_cities)
        
        # Basic specifications
        with st.expander("Basic Dimensions", expanded=True):
            length = st.number_input("Total Length (feet)", min_value=10, step=1, value=50)
            width = st.number_input("Total Width (feet)", min_value=10, step=1, value=30)
            num_floors = st.radio("Number of Floors", options=[1, 2, 3], horizontal=True)
        
        # Room requirements
        with st.expander("Room Requirements", expanded=True):
            bedrooms = st.number_input("Number of Bedrooms", min_value=1, step=1, value=3)
            bathrooms = st.number_input("Number of Bathrooms", min_value=1, step=1, value=2)
            
            # Room types with checkboxes
            st.subheader("Essential Rooms")
            kitchen = st.checkbox("Kitchen", value=True)
            living_room = st.checkbox("Living Room", value=True)
            dining_room = st.checkbox("Dining Room", value=True)
            
            st.subheader("Additional Rooms")
            office = st.checkbox("Home Office")
            laundry = st.checkbox("Laundry Room", value=True)
            pantry = st.checkbox("Pantry")
            mudroom = st.checkbox("Mudroom")
            basement = st.checkbox("Basement")
            
        # Design preferences
        with st.expander("Design Preferences"):
            house_style = st.selectbox(
                "House Style",
                options=["Modern", "Traditional", "Contemporary", "Farmhouse", "Minimalist", "Mediterranean", "Custom"]
            )
            
            if house_style == "Custom":
                custom_style = st.text_input("Describe your custom style")
            
            layout_preference = st.selectbox(
                "Layout Preference",
                options=["Open Floor Plan", "Compartmentalized", "Mixed"]
            )
            
            accessibility = st.checkbox("Include Accessibility Features")
            if accessibility:
                accessibility_features = st.multiselect(
                    "Select Accessibility Features",
                    options=["Wider Doorways", "Ramps", "No Steps", "Accessible Bathroom", "Lower Countertops"]
                )
        
        # Outdoor features
        with st.expander("Outdoor Features"):
            garage_options = st.radio("Garage", options=["None", "1-Car", "2-Car", "3-Car"], horizontal=True)
            
            outdoor_spaces = st.multiselect(
                "Outdoor Spaces",
                options=["Patio", "Deck", "Balcony", "Porch", "Garden", "Pool", "Outdoor Kitchen"],
                default=["Patio"]
            )
            
        # Additional details
        with st.expander("Additional Details"):
            features = st.text_area(
                "Other Features or Requirements (comma-separated)",
                value="walk-in closet, pantry, large windows"
            )
            
            special_instructions = st.text_area(
                "Special Instructions for the AI",
                placeholder="E.g., 'Make the master bedroom face east for morning sunlight'"
            )
    
    with col2:
        st.header("🏗️ Preview & Generate")
        
        # Visualization style options
        render_style = st.selectbox(
            "Rendering Style",
            options=[
                "Blueprint (2D)",
                "Detailed Floor Plan (2D)",
                "3D Floor Plan",
                "Isometric View"
            ]
        )
        
        furniture_detail = st.slider("Furniture Detail Level", min_value=0, max_value=3, value=2, 
                                    help="0: No furniture, 3: Highly detailed furniture")
        
        # Color scheme
        color_scheme = st.radio(
            "Color Scheme",
            options=["Blueprint (Blue/White)", "Grayscale", "Colored"],
            horizontal=True
        )
        
        # Resolution settings
        resolution = st.select_slider(
            "Image Resolution",
            options=["Standard", "High", "Ultra High"],
            value="High"
        )
        
        # Generate button with loading animation
        if st.button("Generate Plan 🚀", type="primary"):
            # Build list of selected rooms
            selected_rooms = []
            if kitchen: selected_rooms.append("kitchen")
            if living_room: selected_rooms.append("living room")
            if dining_room: selected_rooms.append("dining room")
            if office: selected_rooms.append("home office")
            if laundry: selected_rooms.append("laundry room")
            if pantry: selected_rooms.append("pantry")
            if mudroom: selected_rooms.append("mudroom")
            if basement: selected_rooms.append("basement")
            
            # Add garage if selected
            if garage_options != "None":
                selected_rooms.append(garage_options + " garage")
            
            # Add outdoor spaces
            for space in outdoor_spaces:
                selected_rooms.append(space.lower())
            
            # Add bedrooms and bathrooms
            selected_rooms.append(f"{bedrooms} bedrooms")
            selected_rooms.append(f"{bathrooms} bathrooms")
            
            # Additional features
            if features.strip():
                selected_rooms.extend([f.strip() for f in features.split(",")])
            
            # Accessibility features if selected
            if accessibility and accessibility_features:
                for feature in accessibility_features:
                    selected_rooms.append(feature.lower())
            
            # Style specifications
            style_specs = []
            style_specs.append(f"{house_style if house_style != 'Custom' else custom_style} style")
            style_specs.append(f"{layout_preference} layout")
            
            # Build detailed image generation prompt
            prompt = f"""
            Generate a high-quality {render_style.lower()} of a {house_style.lower() if house_style != 'Custom' else custom_style.lower()} house with {num_floors} floor(s) and the following specifications:
            - Total house size: {length} feet long and {width} feet wide
            - Include all these spaces: {', '.join(selected_rooms)}
            - Layout style: {layout_preference}
            
            Rendering Requirements:
            - Show **room names clearly labeled inside each room**
            - Include **room-by-room dimensions** written inside each room
            - Display **total house dimensions** on the outer boundary (length and width)
            - Add **window and door placements** with appropriate symbols
            - Show **walls and partitions** clearly with solid lines
            - Include furniture at detail level {furniture_detail}/3
            - Use a **{color_scheme}** color scheme
            - Maintain **{resolution.lower()} resolution and clarity**
            - Use **dimension annotations** in feet (ft)
            - Each floor should be clearly labeled if multiple floors
            
            {special_instructions if special_instructions else ""}
            
            Make it easy to understand for architects and homeowners alike.
            """
            
            with st.spinner("🔄 Generating your house plan..."):
                try:
                    # Generate image
                    response = client.images.generate(
                        model="flux",  # or "g4f/image" or preferred image model
                        prompt=prompt,
                        response_format="url"
                    )
                    
                    # Display results
                    image_url = response.data[0].url
                    
                    # Store image data and timestamp in session state
                    # Get image data
                    img_data = requests.get(image_url).content
                    
                    # Store in session state
                    if 'saved_plans' not in st.session_state:
                        st.session_state.saved_plans = []
                    
                    # Create a timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    plan_data = {
                        "timestamp": timestamp,
                        "image_data": img_data,
                        "specs": {
                            "dimensions": f"{length}' x {width}'",
                            "floors": num_floors,
                            "bedrooms": bedrooms,
                            "bathrooms": bathrooms,
                            "style": house_style if house_style != "Custom" else custom_style,
                            "render_style": render_style
                        }
                    }
                    
                    st.session_state.saved_plans.append(plan_data)
                    st.session_state.current_plan = plan_data
                    
                    # Show success message
                    st.success("🎉 Your house plan has been generated successfully!")
                    
                    # Display the image
                    st.image(image_url, caption="Your Custom House Plan", use_column_width=True)
                    
                    # Download options
                    col_down1, col_down2 = st.columns(2)
                    
                    with col_down1:
                        st.markdown(f"[📥 Download JPG]({image_url})", unsafe_allow_html=True)
                    
                    with col_down2:
                        # Create a download button for PDF (simulated)
                        st.download_button(
                            label="📄 Download as PDF",
                            data=img_data,
                            file_name=f"house_plan_{timestamp.replace(':', '-').replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
                    
                    # Display house specs
                    with st.expander("House Plan Specifications", expanded=True):
                        st.markdown(f"""
                        **House Dimensions:** {length}' x {width}'  
                        **Number of Floors:** {num_floors}  
                        **Bedrooms:** {bedrooms}  
                        **Bathrooms:** {bathrooms}  
                        **Style:** {house_style if house_style != "Custom" else custom_style}  
                        **Layout:** {layout_preference}  
                        **Features:** {', '.join(selected_rooms)}  
                        """)
                    
                except Exception as e:
                    st.error("❌ Failed to generate the house plan.")
                    st.code(str(e))

    # --- New Section: City-based Info ---
    st.header(f"🏙️ City-Specific Info for {selected_city}")
    
    # 1. Material Cost Table (Mock Data)
    st.subheader("Material Cost Estimate & Supplier Contacts")
    material_data = {
        "Chennai": [
            ("Steel (per ton)", "₹60,000", "ABC Steel Traders, 9876543210"),
            ("Bricks (per 1000)", "₹7,000", "Chennai Bricks, 9123456780"),
            ("Cement (per bag)", "₹400", "UltraCem, 9988776655"),
            ("Sand (per unit)", "₹2,500", "River Sand Co, 9090909090")
        ],
        "Coimbatore": [
            ("Steel (per ton)", "₹59,000", "Coimbatore Steel Mart, 9876501234"),
            ("Bricks (per 1000)", "₹6,800", "Kovai Bricks, 9123409876"),
            ("Cement (per bag)", "₹395", "BuildCem, 9988701234"),
            ("Sand (per unit)", "₹2,400", "Kovai Sand Supply, 9090912345")
        ],
        "Madurai": [
            ("Steel (per ton)", "₹58,500", "Madurai Steel, 9876512345"),
            ("Bricks (per 1000)", "₹6,700", "Madurai Bricks, 9123412345"),
            ("Cement (per bag)", "₹390", "Madurai Cement, 9988712345"),
            ("Sand (per unit)", "₹2,350", "Vaigai Sand, 9090923456")
        ],
        "Tiruchirappalli": [
            ("Steel (per ton)", "₹58,000", "Trichy Steel, 9876523456"),
            ("Bricks (per 1000)", "₹6,600", "Trichy Bricks, 9123423456"),
            ("Cement (per bag)", "₹388", "Trichy Cement, 9988723456"),
            ("Sand (per unit)", "₹2,300", "Cauvery Sand, 9090934567")
        ],
        "Salem": [
            ("Steel (per ton)", "₹57,500", "Salem Steel, 9876534567"),
            ("Bricks (per 1000)", "₹6,500", "Salem Bricks, 9123434567"),
            ("Cement (per bag)", "₹385", "Salem Cement, 9988734567"),
            ("Sand (per unit)", "₹2,250", "Salem Sand, 9090945678")
        ],
        "Tirunelveli": [
            ("Steel (per ton)", "₹57,000", "Tirunelveli Steel, 9876545678"),
            ("Bricks (per 1000)", "₹6,400", "Tirunelveli Bricks, 9123445678"),
            ("Cement (per bag)", "₹382", "Tirunelveli Cement, 9988745678"),
            ("Sand (per unit)", "₹2,200", "Tamirabarani Sand, 9090956789")
        ],
        "Tiruppur": [
            ("Steel (per ton)", "₹56,500", "Tiruppur Steel, 9876556789"),
            ("Bricks (per 1000)", "₹6,300", "Tiruppur Bricks, 9123456789"),
            ("Cement (per bag)", "₹380", "Tiruppur Cement, 9988756789"),
            ("Sand (per unit)", "₹2,150", "Noyyal Sand, 9090967890")
        ],
        "Vellore": [
            ("Steel (per ton)", "₹56,000", "Vellore Steel, 9876567890"),
            ("Bricks (per 1000)", "₹6,200", "Vellore Bricks, 9123467890"),
            ("Cement (per bag)", "₹378", "Vellore Cement, 9988767890"),
            ("Sand (per unit)", "₹2,100", "Palar Sand, 9090978901")
        ],
        "Thoothukudi": [
            ("Steel (per ton)", "₹55,500", "Tuticorin Steel, 9876578901"),
            ("Bricks (per 1000)", "₹6,100", "Tuticorin Bricks, 9123478901"),
            ("Cement (per bag)", "₹375", "Tuticorin Cement, 9988778901"),
            ("Sand (per unit)", "₹2,050", "Tuticorin Sand, 9090989012")
        ],
        "Erode": [
            ("Steel (per ton)", "₹55,000", "Erode Steel, 9876589012"),
            ("Bricks (per 1000)", "₹6,000", "Erode Bricks, 9123489012"),
            ("Cement (per bag)", "₹372", "Erode Cement, 9988789012"),
            ("Sand (per unit)", "₹2,000", "Bhavani Sand, 9090990123")
        ],
    }
    city_materials = material_data.get(selected_city, material_data["Chennai"])
    st.table({
        "Material": [row[0] for row in city_materials],
        "Approx. Cost": [row[1] for row in city_materials],
        "Supplier/Contact": [row[2] for row in city_materials]
    })

    # 2. Top 5 Builders & Budget (Mock Data)
    st.subheader("Top 5 Builders & House Model Budget Estimate")
    builder_data = {
        "Chennai": [
            ("L&T Construction", "₹45-60 Lakhs", "044-12345678"),
            ("Prestige Group", "₹50-70 Lakhs", "044-87654321"),
            ("Casa Grande", "₹40-55 Lakhs", "044-23456789"),
            ("Appaswamy Real Estates", "₹48-65 Lakhs", "044-34567890"),
            ("Radiance Realty", "₹42-58 Lakhs", "044-45678901")
        ],
        "Coimbatore": [
            ("Srivari Infrastructure", "₹38-52 Lakhs", "0422-123456"),
            ("VKC Developers", "₹40-54 Lakhs", "0422-654321"),
            ("Sreevatsa Real Estates", "₹36-50 Lakhs", "0422-234567"),
            ("Lancor Holdings", "₹39-53 Lakhs", "0422-345678"),
            ("Chathamkulam Builders", "₹37-51 Lakhs", "0422-456789")
        ],
        "Madurai": [
            ("Madurai Builders", "₹35-48 Lakhs", "0452-123456"),
            ("Vaigai Constructions", "₹36-50 Lakhs", "0452-654321"),
            ("Sree Builders", "₹34-47 Lakhs", "0452-234567"),
            ("Meenakshi Estates", "₹37-49 Lakhs", "0452-345678"),
            ("Pandiyan Realty", "₹33-46 Lakhs", "0452-456789")
        ],
        "Tiruchirappalli": [
            ("Trichy Builders", "₹34-47 Lakhs", "0431-123456"),
            ("Cauvery Estates", "₹35-48 Lakhs", "0431-654321"),
            ("Rockfort Realty", "₹33-46 Lakhs", "0431-234567"),
            ("Srirangam Constructions", "₹36-49 Lakhs", "0431-345678"),
            ("Golden City Builders", "₹32-45 Lakhs", "0431-456789")
        ],
        "Salem": [
            ("Salem Estates", "₹33-46 Lakhs", "0427-123456"),
            ("Steel City Builders", "₹34-47 Lakhs", "0427-654321"),
            ("Shevaroy Realty", "₹32-45 Lakhs", "0427-234567"),
            ("Yercaud Constructions", "₹35-48 Lakhs", "0427-345678"),
            ("Salem Dream Homes", "₹31-44 Lakhs", "0427-456789")
        ],
        "Tirunelveli": [
            ("Nellai Builders", "₹32-45 Lakhs", "0462-123456"),
            ("Tamirabarani Estates", "₹33-46 Lakhs", "0462-654321"),
            ("Pearl City Realty", "₹31-44 Lakhs", "0462-234567"),
            ("Nellai Dream Homes", "₹34-47 Lakhs", "0462-345678"),
            ("Tirunelveli Constructions", "₹30-43 Lakhs", "0462-456789")
        ],
        "Tiruppur": [
            ("Tiruppur Builders", "₹31-44 Lakhs", "0421-123456"),
            ("Noyyal Estates", "₹32-45 Lakhs", "0421-654321"),
            ("Cotton City Realty", "₹30-43 Lakhs", "0421-234567"),
            ("Tiruppur Dream Homes", "₹33-46 Lakhs", "0421-345678"),
            ("Tiruppur Constructions", "₹29-42 Lakhs", "0421-456789")
        ],
        "Vellore": [
            ("Vellore Builders", "₹30-43 Lakhs", "0416-123456"),
            ("Palar Estates", "₹31-44 Lakhs", "0416-654321"),
            ("Fort City Realty", "₹29-42 Lakhs", "0416-234567"),
            ("Vellore Dream Homes", "₹32-45 Lakhs", "0416-345678"),
            ("Vellore Constructions", "₹28-41 Lakhs", "0416-456789")
        ],
        "Thoothukudi": [
            ("Tuticorin Builders", "₹29-42 Lakhs", "0461-123456"),
            ("Pearl City Estates", "₹30-43 Lakhs", "0461-654321"),
            ("Harbour Realty", "₹28-41 Lakhs", "0461-234567"),
            ("Tuticorin Dream Homes", "₹31-44 Lakhs", "0461-345678"),
            ("Tuticorin Constructions", "₹27-40 Lakhs", "0461-456789")
        ],
        "Erode": [
            ("Erode Builders", "₹28-41 Lakhs", "0424-123456"),
            ("Bhavani Estates", "₹29-42 Lakhs", "0424-654321"),
            ("Textile City Realty", "₹27-40 Lakhs", "0424-234567"),
            ("Erode Dream Homes", "₹30-43 Lakhs", "0424-345678"),
            ("Erode Constructions", "₹26-39 Lakhs", "0424-456789")
        ],
    }
    city_builders = builder_data.get(selected_city, builder_data["Chennai"])
    st.table({
        "Builder": [row[0] for row in city_builders],
        "Approx. Budget": [row[1] for row in city_builders],
        "Contact": [row[2] for row in city_builders]
    })

    # 3. Project Timeline Estimation (Mock Data)
    st.subheader("Project Timeline Estimation")
    st.markdown("""
    | Phase                | Duration (weeks) |
    |----------------------|------------------|
    | Design & Planning    | 2-4              |
    | Approvals & Permits  | 2-6              |
    | Site Preparation     | 1-2              |
    | Foundation           | 2-3              |
    | Structure & Walls    | 4-6              |
    | Roofing              | 2                |
    | Finishing & Interiors| 6-10             |
    | Handover             | 1                |
    | **Total**            | **20-34**        |
    """)

    # 4. Solar Panel Companies & Cost (Mock Data)
    st.subheader("Energy Efficiency: Solar Panel Companies & Cost Estimate")
    solar_data = {
        "Chennai": [
            ("Tata Power Solar", "₹80,000 - ₹1,20,000 (3kW)", "1800-419-8777"),
            ("Vikram Solar", "₹78,000 - ₹1,15,000 (3kW)", "1800-212-8200"),
            ("Waaree Energies", "₹75,000 - ₹1,10,000 (3kW)", "1800-2121-321"),
        ],
        "Coimbatore": [
            ("RenewSys Solar", "₹77,000 - ₹1,12,000 (3kW)", "1800-102-3775"),
            ("Adani Solar", "₹79,000 - ₹1,18,000 (3kW)", "1800-123-5555"),
        ],
        "Madurai": [
            ("Luminous Solar", "₹76,000 - ₹1,10,000 (3kW)", "1800-300-2945"),
            ("Havells Solar", "₹78,000 - ₹1,13,000 (3kW)", "1800-103-1313"),
        ],
        "Tiruchirappalli": [
            ("Microtek Solar", "₹75,000 - ₹1,09,000 (3kW)", "1800-102-4447"),
            ("Goldi Solar", "₹77,000 - ₹1,12,000 (3kW)", "1800-258-5555"),
        ],
        "Salem": [
            ("Exide Solar", "₹74,000 - ₹1,08,000 (3kW)", "1800-103-5454"),
            ("Jakson Solar", "₹76,000 - ₹1,11,000 (3kW)", "1800-103-2600"),
        ],
        "Tirunelveli": [
            ("Emmvee Solar", "₹73,000 - ₹1,07,000 (3kW)", "1800-425-4455"),
            ("Navitas Solar", "₹75,000 - ₹1,10,000 (3kW)", "1800-233-2303"),
        ],
        "Tiruppur": [
            ("Solex Solar", "₹72,000 - ₹1,06,000 (3kW)", "1800-200-6006"),
            ("Surana Solar", "₹74,000 - ₹1,09,000 (3kW)", "1800-425-0111"),
        ],
        "Vellore": [
            ("Photon Energy", "₹71,000 - ₹1,05,000 (3kW)", "1800-200-0101"),
            ("Sunshot Solar", "₹73,000 - ₹1,08,000 (3kW)", "1800-200-1234"),
        ],
        "Thoothukudi": [
            ("SunEdison", "₹70,000 - ₹1,04,000 (3kW)", "1800-200-5005"),
            ("Swelect Solar", "₹72,000 - ₹1,07,000 (3kW)", "1800-200-5555"),
        ],
        "Erode": [
            ("Insolation Energy", "₹69,000 - ₹1,03,000 (3kW)", "1800-200-7007"),
            ("Ujaas Solar", "₹71,000 - ₹1,06,000 (3kW)", "1800-233-2303"),
        ],
    }
    city_solar = solar_data.get(selected_city, solar_data["Chennai"])
    st.table({
        "Company": [row[0] for row in city_solar],
        "Approx. Cost": [row[1] for row in city_solar],
        "Contact": [row[2] for row in city_solar]
    })

    # 5. Legal & Permit Guidance (Mock Data)
    st.subheader("Legal & Permit Guidance")
    st.markdown("""
    **For House Construction:**
    - Land Ownership Documents (Patta, Chitta, EC)
    - Building Plan Approval from Local Authority (CMDA/DTCP/Corporation/Municipality)
    - Planning Permission
    - Structural Stability Certificate
    - NOC from Fire, Water, and Electricity Departments
    - Commencement Certificate
    - Completion Certificate
    - Property Tax Assessment
    
    **For Commercial Building:**
    - All of the above, plus:
    - Trade License
    - Environmental Clearance (if applicable)
    - Lift Installation Approval (if applicable)
    - Fire Safety Certificate (mandatory)
    
    **Process:**
    1. Submit application with required documents to local authority
    2. Pay prescribed fees
    3. Site inspection by officials
    4. Obtain plan approval and permits
    5. Start construction
    6. Obtain completion certificate after construction
    """)

with tab2:
    st.header("💾 My Saved Plans")
    
    if 'saved_plans' not in st.session_state or not st.session_state.saved_plans:
        st.info("You haven't generated any plans yet. Go to the 'Generate Plan' tab to create one!")
    else:
        # Display saved plans
        for i, plan in enumerate(st.session_state.saved_plans):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Convert image data to display
                image_bytes = BytesIO(plan["image_data"])
                st.image(image_bytes, width=200)
            
            with col2:
                st.markdown(f"**Plan #{i+1}** - Generated on {plan['timestamp']}")
                st.markdown(f"""
                - **Dimensions:** {plan['specs']['dimensions']}
                - **Floors:** {plan['specs']['floors']}
                - **Bedrooms:** {plan['specs']['bedrooms']}
                - **Bathrooms:** {plan['specs']['bathrooms']}
                - **Style:** {plan['specs']['style']}
                """)
                
                # Action buttons
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                
                with btn_col1:
                    st.download_button(
                        "📥 Download",
                        data=plan["image_data"],
                        file_name=f"house_plan_{plan['timestamp'].replace(':', '-').replace(' ', '_')}.jpg",
                        mime="image/jpeg"
                    )
                
                with btn_col2:
                    if st.button(f"🔄 Regenerate #{i+1}", key=f"regen_{i}"):
                        st.session_state.regenerate_plan = i
                        st.experimental_rerun()
                
                with btn_col3:
                    if st.button(f"🗑️ Delete #{i+1}", key=f"del_{i}"):
                        # Add confirmation
                        st.session_state.delete_plan = i
                        st.warning(f"Are you sure you want to delete Plan #{i+1}?")
                        
                        conf_col1, conf_col2 = st.columns(2)
                        with conf_col1:
                            if st.button("✓ Yes, Delete", key=f"confirm_del_{i}"):
                                st.session_state.saved_plans.pop(i)
                                st.experimental_rerun()
                        with conf_col2:
                            if st.button("✗ Cancel", key=f"cancel_del_{i}"):
                                del st.session_state.delete_plan
                                st.experimental_rerun()
            
            st.markdown("---")
        
        # Clear all button
        if st.button("🗑️ Clear All Plans"):
            st.warning("Are you sure you want to delete all your saved plans? This cannot be undone.")
            
            conf_col1, conf_col2 = st.columns(2)
            with conf_col1:
                if st.button("✓ Yes, Delete All", key="confirm_del_all"):
                    st.session_state.saved_plans = []
                    st.experimental_rerun()
            with conf_col2:
                if st.button("✗ Cancel", key="cancel_del_all"):
                    st.experimental_rerun()

with tab3:
    st.header("ℹ️ Help & Tips")
    
    with st.expander("How to Use This App", expanded=True):
        st.markdown("""
        **Step 1:** Enter your house specifications in the form
        - Set the overall dimensions
        - Specify the number of bedrooms and bathrooms
        - Select additional rooms and features
        
        **Step 2:** Set your design preferences
        - Choose a house style
        - Select a layout preference
        - Add any accessibility features needed
        
        **Step 3:** Choose rendering options
        - Select the visualization style
        - Set the furniture detail level
        - Choose a color scheme
        
        **Step 4:** Generate your plan
        - Click the "Generate Plan" button
        - Wait for the AI to create your custom blueprint
        - Download or save your plan
        """)
    
    with st.expander("Tips for Better Results"):
        st.markdown("""
        1. **Be specific with dimensions** - Providing realistic proportions will yield better results
        2. **Balance features and space** - Don't try to fit too many rooms in a small footprint
        3. **Include special instructions** - Guide the AI with specific requirements about layout or room placement
        4. **Try different styles** - Each rendering style offers a different perspective on your design
        5. **Start simple, then add details** - Create a basic plan first, then regenerate with more specific requirements
        """)
    
    with st.expander("Example Feature Combinations"):
        st.markdown("""
        **Cozy Family Home:**
        - 3 bedrooms, 2 bathrooms
        - Open floor plan
        - Kitchen with island, dining area, living room
        - Master suite with walk-in closet
        - Patio and 2-car garage
        
        **Minimalist Modern Dwelling:**
        - 2 bedrooms, 1 bathroom
        - Open concept design
        - Large windows, high ceilings
        - Compact but functional kitchen
        - Small home office nook
        
        **Luxury Estate:**
        - 4+ bedrooms, 3+ bathrooms
        - Formal dining room, chef's kitchen, butler's pantry
        - Home office, media room, game room
        - Master suite with sitting area and spa bathroom
        - 3-car garage, pool, outdoor kitchen
        """)
    
    with st.expander("Understanding Floor Plans"):
        st.markdown("""
        **Common Symbols:**
        - Solid lines represent walls
        - Thin lines with gaps represent windows
        - Arcs represent door swings
        - Small rectangles may represent fixtures like sinks, toilets, etc.
        
        **Measurements:**
        - Dimensions are typically shown in feet and inches
        - Room sizes are usually measured from interior wall to interior wall
        - Overall dimensions include exterior walls
        
        **Orientation:**
        - North is typically at the top of the plan unless otherwise noted
        - Consider sun exposure when placing rooms (e.g., bedrooms facing east get morning sun)
        """)
    
    with st.expander("Legal Disclaimer"):
        st.markdown("""
        **Disclaimer:**
        The floor plans generated by this application are conceptual in nature and are intended for visualization purposes only. They are not construction documents and should not be used for building without proper review and modification by a licensed architect or engineer.
        
        The dimensions, room layouts, and structural elements shown may not comply with local building codes, zoning regulations, or other requirements. Always consult with a professional before proceeding with any construction project.
        """)

# Footer
st.markdown("---")
st.markdown("© 2025 AI House Plan Generator | Made with ❤️ using Streamlit and AI")

# Configure page theme
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)