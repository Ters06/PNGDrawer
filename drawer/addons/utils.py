# drawer/addons/utils.py
import math

def draw_dashed_path(draw, path, color, width, dash_length):
    """
    Draws a dashed or dotted line along a complex path (a list of points).
    This maintains the dash pattern continuously across all segments of the path.
    """
    is_drawing = True
    distance_in_dash = 0
    
    for i in range(len(path) - 1):
        p1 = path[i]
        p2 = path[i+1]
        
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        segment_length = math.hypot(dx, dy)
        if segment_length == 0:
            continue
        
        unit_dx, unit_dy = dx / segment_length, dy / segment_length
        
        current_distance_on_segment = 0
        while current_distance_on_segment < segment_length:
            remaining_in_pattern = dash_length - distance_in_dash
            step = min(remaining_in_pattern, segment_length - current_distance_on_segment)
            
            p_start = (p1[0] + unit_dx * current_distance_on_segment, p1[1] + unit_dy * current_distance_on_segment)
            p_end = (p1[0] + unit_dx * (current_distance_on_segment + step), p1[1] + unit_dy * (current_distance_on_segment + step))
            
            if is_drawing:
                # Ensure coordinates are integers for the drawing call
                line_segment = [
                    (int(p_start[0]), int(p_start[1])),
                    (int(p_end[0]), int(p_end[1]))
                ]
                draw.line(line_segment, fill=color, width=width)
            
            distance_in_dash += step
            if distance_in_dash >= dash_length:
                distance_in_dash = 0
                is_drawing = not is_drawing
                
            current_distance_on_segment += step
