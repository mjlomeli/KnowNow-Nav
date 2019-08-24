#Jennifer Kwon

""" Before using this function, you must use the neo4j driver for Python. Refer to Neo4jDriver.py.

  After exporting the style.grass file from neo4j, run this function on a Python IDE and pass 
  node_label: "Category tag", opacity: 0.1 as parameters.
  In your directory, file new_style.grass will be created and you must manually import it onto neo4j.
 
"""
    def change_opacity_of_node(self, node_label: str, opacity: float):
        
        with open("style.grass", 'r', newline="") as file_object:

            nodes_styles = file_object.readlines()
            
        with open("new_style.grass", 'w') as file_object_2:
                
            i = 0
            
            while i < len(nodes_styles):
               
                if node_label in nodes_styles[i]:
                    
                    file_object_2.write(nodes_styles[i])

                    
                    if "color: " not in nodes_styles[i]:
                        i+=1
                        
                    if "color: " in nodes_styles[i]:

                        # Get color of node
                        old_node_color = style_list[i][9:16]

                        # Change hex to rgb tuple
                        hex_color = old_node_color_lstrip('#')
                        
                        rgb_color = tuple(int(h[i:i+2], 16) for i in (0,2,4))
                        
                        # Convert rgb to rgba

                        # Write to style.grass file
                        file_object_2.write("opacity: ")
                else:
                    file_object_2.write(nodes_styles[i]) 
                    i+=1  
        return
