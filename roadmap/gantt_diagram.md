```mermaid
gantt
        title Gantt diagram project
        dateFormat  YYYY-MM-DD
        axisFormat %d-%m
        section Research
            Data search :2024-10-01, 2024-10-25
        section Meetings
            Meeting :after MER_ART, 2024-10-02, 1d
            Meeting :after MER_ART, 2024-10-08, 1d
            Meeting :after MER_ART, 2024-10-16, 1d
            Meeting :after MER_ART, 2024-10-21, 1d
            Meeting :after MER_ART, 2024-11-06, 1d 
            Meeting :after MER_ART, 2024-11-13, 1d 
            Meeting :after MER_ART, 2024-11-20, 1d
            Meeting :after MER_ART, 2024-11-27, 1d 
            Meeting :after MER_ART, 2024-12-04, 1d
            Meeting :after MER_ART, 2024-12-11, 1d
        section Developement
            Main code, tests, web dev :2024-10-25, 2024-12-04
            Oral : 2024-12-04, 2024-12-11 
        section Deadlines
            ! Last push   :milestone, crit, 2024-12-10, 1d
            Mid-term    :crit, 2024-10-25, 1d
        section Final
            Oral presentation    :crit, 2024-12-13, 1d
