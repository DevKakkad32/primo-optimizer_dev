#################################################################################
# PRIMO - The P&A Project Optimizer was produced under the Methane Emissions Reduction Program (MERP)
# and National Energy Technology Laboratory's (NETL) National Emissions Reduction Initiative (NEMRI).
#
# NOTICE. This Software was developed under funding from the U.S. Government and the U.S.
# Government consequently retains certain rights. As such, the U.S. Government has been granted for
# itself and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide license in
# the Software to reproduce, distribute copies to the public, prepare derivative works, and perform
# publicly and display publicly, and to permit others to do so.
#################################################################################

# Standard libs
from math import isnan
from typing import Tuple, List

# Installed libs

# User defined libs


class OptimalProject:
    """
    Represents an optimal project for plugging and abandonment (P&A) based on the provided well data.

    Parameters
    ----------
    cluster : str
        The name or identifier of the project cluster.
    well_dict : dict
        A dictionary where keys are well IDs and values contain well information.
    plugging_cost : dict
        A dictionary mapping the number of wells to the corresponding plugging cost.
    well_data : dict
        A dictionary where keys are well IDs and values contain detailed well information.

    Attributes
    ----------
    project_name : str
        The name or identifier of the project cluster.
    well_list : dict
        A dictionary where keys are well IDs and values contain well information.
    num_wells : int
        The number of wells in the project.
    plugging_cost : dict
        A dictionary mapping the number of wells to the corresponding plugging cost.
    well_data : dataframe
        A dataframe with well IDs and contain detailed well information.
    """

    def __init__(self, cluster, well_dict, plugging_cost, well_data):
        self.project_name = cluster
        self.well_list = well_dict
        self.num_wells = len(well_dict)
        self.plugging_cost = plugging_cost
        self.well_data = well_data

    def impact_score(self) -> float:
        """
        Calculate the total impact score of the project based on well data.

        Returns
        -------
        float
            The total impact score for the project.
        """
        total_impact_score = 0
        for well_id in self.well_list:
            if well_id in self.well_data and "Impact Score" in self.well_data[well_id]:
                total_impact_score += self.well_data[well_id]["Impact Score"]
        return total_impact_score

    def total_plugging_cost(self) -> float:
        """
        Calculate the total cost to plug all wells in the project.

        Returns
        -------
        float
            The total plugging cost for the project.
        """
        total_plugging_cost = self.plugging_cost[self.num_wells]
        return total_plugging_cost

    def age_range(self) -> Tuple[float, List[str]]:
        """
        Calculate the range of ages for wells in the project and provide warnings for missing data.

        Returns
        -------
        Tuple[float, List[str]]
            A tuple where the first element is the range of ages (max - min) and
            the second element is a list of warnings regarding missing or zero age information.
        """
        ages = []
        warnings = []
        for well_id in self.well_list:
            if well_id in self.well_data and "Age [years]" in self.well_data[well_id]:
                age = self.well_data[well_id]["Age [years]"]
                if age == 0 or age is None or isnan(age):
                    warnings.append(
                        f"Warning: Age information for well {well_id} not available, estimated to be average age of other wells in the project."
                    )
                else:
                    ages.append(age)

        # Calculate average age for wells with non-zero age
        if ages:
            avg_age = sum(ages) / len(ages)
        else:
            avg_age = 100  # Default value if no ages are available

        # Substitute missing or zero ages with the average age
        for well_id in self.well_list:
            if well_id in self.well_data and "Age [years]" in self.well_data[well_id]:
                age = self.well_data[well_id]["Age [years]"]
                if age == 0 or age is None or isnan(age):
                    ages.append(avg_age)

        if ages:
            age_range = max(ages) - min(ages)
        else:
            age_range = 0  # If no ages are available, the range is zero

        return age_range, warnings

    def depth_range(self) -> Tuple[float, List[str]]:
        """
        Calculate the range of depths for wells in the project and provide warnings for missing data.

        Returns
        -------
        Tuple[float, List[str]]
            A tuple where the first element is the range of depths (max - min) and
            the second element is a list of warnings regarding missing or zero depth information.
        """
        depths = []
        warnings = []
        for well_id in self.well_list:
            if well_id in self.well_data and "Depth [ft]" in self.well_data[well_id]:
                depth = self.well_data[well_id]["Depth [ft]"]
                if (
                    depth == 0
                    or depth is None
                    or (isinstance(depth, float) and isnan(depth))
                ):
                    warnings.append(
                        f"Warning: Depth information for well {well_id} not available."
                    )
                else:
                    depths.append(depth)

        if depths:
            depth_range = max(depths) - min(depths)
        else:
            depth_range = 0  # If no depths are available, the range is zero

        return depth_range, warnings

    def num_wells_sensitive_receptors(self) -> int:
        """
        Calculate the number of wells in the project that are near sensitive receptors.

        Returns
        -------
        int
            The total number of sensitive receptors near the wells.
        """
        count = 0
        for well_id in self.well_list:
            if well_id in self.well_data:
                well_info = self.well_data[well_id]
                schools_within_distance = well_info.get("Schools Within Distance", 0)
                hospitals_within_distance = well_info.get(
                    "Hospitals Within Distance", 0
                )
                buildings_within_short_distance = well_info.get(
                    "Buildings (0 - 300 ft)", "No"
                )
                buildings_within_distance = well_info.get(
                    "Buildings (300 - 1320 ft)", "No"
                )
                count += schools_within_distance
                count += hospitals_within_distance
                if buildings_within_short_distance == "Yes":
                    count += 1
                if buildings_within_distance == "Yes":
                    count += 1
        return count

    def num_wells_dac(self) -> int:
        """
        Calculate the number of wells in the project that are located in disadvantaged communities.

        Returns
        -------
        int
            The number of wells in disadvantaged communities.
        """
        count = 0
        for well_id in self.well_list:
            if (
                well_id in self.well_data
                and self.well_data[well_id].get("Disadvantaged Community", 0) == 1
            ):
                count += 1
        return count

    def population_density(self) -> float:
        """
        Calculate the average population density around the wells in the project.

        Returns
        -------
        float
            The average population density for the project.
        """
        total_population_density = 0
        valid_count = 0
        for well_id in self.well_list:
            if (
                well_id in self.well_data
                and "Population Density" in self.well_data[well_id]
            ):
                density = self.well_data[well_id]["Population Density"]
                total_population_density += density
                valid_count += 1

        if valid_count > 0:
            avg_density = total_population_density / valid_count
        else:
            avg_density = 0

        return avg_density


class OptimalCampaign:
    """
    Represents an optimal campaign that consists of multiple projects.

    Parameters
    ----------
    clusters_dict : dict
        A dictionary where keys are cluster names and values are dictionaries of wells for each cluster.

    Attributes
    ----------
    clusters_dict : dict
        A dictionary where keys are cluster names and values are dictionaries of wells for each cluster.
    projects : dict
        A dictionary where keys are project names and values are `OptimalProject` instances.
    """

    def __init__(self, clusters_dict):
        self.clusters_dict = clusters_dict
        self.projects = {}

    def build_projects(self) -> None:
        """
        Build `OptimalProject` instances for each cluster and store them in the `projects` attribute.
        """
        for cluster, well_dict in self.clusters_dict.items():
            plugging_cost = self.calculate_plugging_cost()
            well_data = self.get_well_data(cluster, well_dict)
            project = OptimalProject(cluster, well_dict, plugging_cost, well_data)
            setattr(self, f"project_{cluster}", project)
            self.projects[cluster] = project

    def overall_impact(self) -> float:
        """
        Calculate the total impact score across all projects.

        Returns
        -------
        float
            The total impact score for the campaign.
        """
        total_impact = 0
        for project in self.projects.values():
            total_impact += project.impact_score()
        return total_impact

    def num_wells_dac(self) -> int:
        """
        Calculate the total number of wells in disadvantaged communities across all projects.

        Returns
        -------
        int
            The total number of wells in disadvantaged communities for the campaign.
        """
        total_dac_wells = 0
        for project in self.projects.values():
            total_dac_wells += project.num_wells_dac()
        return total_dac_wells

    def num_wells_sensitive_receptors(self) -> int:
        """
        Calculate the total number of sensitive receptors near wells across all projects.

        Returns
        -------
        int
            The total number of sensitive receptors for the campaign.
        """
        total_sensitive_receptors = 0
        for project in self.projects.values():
            total_sensitive_receptors += project.num_wells_sensitive_receptors()
        return total_sensitive_receptors

    def calculate_plugging_cost(self):
        """
        Calculate the total plugging cost for a campaign across all projects.

        :param cluster: Name of the project cluster.
        :param well_dict: Dictionary of wells in the project.
        :return: Total plugging cost for the campaign.
        """
        total_campaign_cost = 0
        for project in self.projects.values():
            total_campaign_cost += project.total_plugging_cost()
        return total_campaign_cost

    # def get_well_data(self, cluster, well_dict):
    #     """
    #     Retrieve the well data for a specific cluster.

    #     :param cluster: Name of the project cluster.
    #     :param well_dict: Dictionary of wells in the project.
    #     :return: Dictionary of well data for the cluster.
    #     """
    #     # Implement the logic for getting the well data for a cluster
    #     return {}  # Placeholder
