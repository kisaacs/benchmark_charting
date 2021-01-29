from data_model import ChartingDataModel, ChartWrapper


def test_data_model():
    db = ChartingDataModel()
    db.add_settings('blazemark_base_path', 'c')
    ch = ChartWrapper("Dmatd", "chunk_size", "Mflops")
    ch.add_chart_legends(db,"chunk_size", 3)
    ch.add_chart_legends(db,"Mflops", 50)
    ch.add_chart_legends(db,"block_size", 10)
    # n_uid = c.create_chart("my_chart")
    # c.add_new_datapoint(n_uid, "blazemark")


if __name__ == '__main__':
    print("Hello from benchmark charting")
    test_data_model()
