from sqlmodel import create_engine


DATABASE_URL = "sqlite:///lost_and_found_t1.db"
connect_args = {"check_same_thread": False}


engine = create_engine(DATABASE_URL, connect_args=connect_args)

